"""
SLA113 Iteration 15 Tests - Job Dependencies Feature
Tests: dependency tracking, blocked status, auto-unblock, graph endpoint, link/unlink APIs
"""
import pytest
import requests
import os
import time

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')
API = f"{BASE_URL}/api/sla113"


class TestJobDependencies:
    """Test job dependency creation and blocked status"""
    
    def test_create_job_without_dependencies(self):
        """Job without dependencies should be 'pending'"""
        response = requests.post(f"{API}/jobs", json={
            "preset": "ARCADE_40",
            "priority": "normal"
        })
        assert response.status_code == 200
        job = response.json()
        assert job["status"] == "pending"
        assert job.get("depends_on", []) == []
        # Cleanup
        requests.delete(f"{API}/jobs/{job['id']}")
    
    def test_create_job_with_completed_dependency(self):
        """Job with completed parent should be 'pending'"""
        # Create parent job
        parent_res = requests.post(f"{API}/jobs", json={"preset": "ARCADE_40", "priority": "high"})
        parent = parent_res.json()
        parent_id = parent["id"]
        
        # Wait for parent to complete (worker processes every 3s)
        for _ in range(30):  # Max 90 seconds
            time.sleep(3)
            check = requests.get(f"{API}/jobs")
            jobs = check.json().get("jobs", [])
            parent_job = next((j for j in jobs if j["id"] == parent_id), None)
            if parent_job and parent_job["status"] == "completed":
                break
        
        # Create child with completed parent
        child_res = requests.post(f"{API}/jobs", json={
            "preset": "SLOTS_20",
            "priority": "normal",
            "depends_on": [parent_id]
        })
        child = child_res.json()
        
        # Child should be pending since parent is complete
        assert child["status"] == "pending"
        assert parent_id in child.get("depends_on", [])
        
        # Cleanup
        requests.delete(f"{API}/jobs/{child['id']}")
        requests.delete(f"{API}/jobs/{parent_id}")
    
    def test_create_job_with_incomplete_dependency_is_blocked(self):
        """Job with incomplete parent should be 'blocked'"""
        # Create parent job
        parent_res = requests.post(f"{API}/jobs", json={"preset": "FANTASY_RPG", "priority": "low"})
        parent = parent_res.json()
        parent_id = parent["id"]
        
        # Immediately create child (parent won't be complete yet)
        child_res = requests.post(f"{API}/jobs", json={
            "preset": "COD_WARFARE",
            "priority": "normal",
            "depends_on": [parent_id]
        })
        child = child_res.json()
        
        # Child should be blocked
        assert child["status"] == "blocked", f"Expected blocked, got {child['status']}"
        assert parent_id in child.get("depends_on", [])
        
        # Cleanup
        requests.delete(f"{API}/jobs/{child['id']}")
        requests.delete(f"{API}/jobs/{parent_id}")
    
    def test_invalid_dependency_returns_400(self):
        """Creating job with non-existent dependency should fail"""
        response = requests.post(f"{API}/jobs", json={
            "preset": "ARCADE_40",
            "depends_on": ["NONEXISTENT-JOB-ID"]
        })
        assert response.status_code == 400
        assert "not found" in response.json().get("detail", "").lower()


class TestLinkUnlinkAPIs:
    """Test POST /jobs/{id}/link and DELETE /jobs/{id}/link/{dep_id}"""
    
    def test_link_dependency(self):
        """POST /jobs/{id}/link should add dependency"""
        # Create two jobs
        job1_res = requests.post(f"{API}/jobs", json={"preset": "ARCADE_40"})
        job1 = job1_res.json()
        job2_res = requests.post(f"{API}/jobs", json={"preset": "SLOTS_20"})
        job2 = job2_res.json()
        
        # Link: job2 depends on job1
        link_res = requests.post(f"{API}/jobs/{job2['id']}/link?depends_on_id={job1['id']}")
        assert link_res.status_code == 200
        link_data = link_res.json()
        assert link_data.get("linked") == True
        assert link_data.get("job") == job2["id"]
        assert link_data.get("depends_on") == job1["id"]
        
        # Verify job2 now has dependency
        jobs_res = requests.get(f"{API}/jobs")
        jobs = jobs_res.json().get("jobs", [])
        job2_updated = next((j for j in jobs if j["id"] == job2["id"]), None)
        assert job1["id"] in job2_updated.get("depends_on", [])
        
        # Cleanup
        requests.delete(f"{API}/jobs/{job1['id']}")
        requests.delete(f"{API}/jobs/{job2['id']}")
    
    def test_unlink_dependency(self):
        """DELETE /jobs/{id}/link/{dep_id} should remove dependency"""
        # Create parent and child with dependency
        parent_res = requests.post(f"{API}/jobs", json={"preset": "ARCADE_40"})
        parent = parent_res.json()
        child_res = requests.post(f"{API}/jobs", json={"preset": "SLOTS_20", "depends_on": [parent["id"]]})
        child = child_res.json()
        
        # Verify child has dependency
        assert parent["id"] in child.get("depends_on", [])
        
        # Unlink
        unlink_res = requests.delete(f"{API}/jobs/{child['id']}/link/{parent['id']}")
        assert unlink_res.status_code == 200
        assert unlink_res.json().get("unlinked") == True
        
        # Verify dependency removed
        jobs_res = requests.get(f"{API}/jobs")
        jobs = jobs_res.json().get("jobs", [])
        child_updated = next((j for j in jobs if j["id"] == child["id"]), None)
        assert parent["id"] not in child_updated.get("depends_on", [])
        
        # Cleanup
        requests.delete(f"{API}/jobs/{parent['id']}")
        requests.delete(f"{API}/jobs/{child['id']}")
    
    def test_link_nonexistent_job_returns_404(self):
        """Linking non-existent jobs should return 404"""
        response = requests.post(f"{API}/jobs/FAKE-JOB/link?depends_on_id=FAKE-PARENT")
        assert response.status_code == 404
    
    def test_circular_dependency_prevented(self):
        """Circular dependencies should be prevented"""
        # Create job1 and job2
        job1_res = requests.post(f"{API}/jobs", json={"preset": "ARCADE_40"})
        job1 = job1_res.json()
        job2_res = requests.post(f"{API}/jobs", json={"preset": "SLOTS_20", "depends_on": [job1["id"]]})
        job2 = job2_res.json()
        
        # Try to make job1 depend on job2 (circular)
        circular_res = requests.post(f"{API}/jobs/{job1['id']}/link?depends_on_id={job2['id']}")
        # Should return 400 for circular dependency
        assert circular_res.status_code == 400
        
        # Cleanup
        requests.delete(f"{API}/jobs/{job1['id']}")
        requests.delete(f"{API}/jobs/{job2['id']}")


class TestDependencyGraph:
    """Test GET /jobs/graph endpoint"""
    
    def test_graph_returns_nodes_and_edges(self):
        """Graph endpoint should return nodes and edges"""
        response = requests.get(f"{API}/jobs/graph")
        assert response.status_code == 200
        data = response.json()
        assert "nodes" in data
        assert "edges" in data
        assert isinstance(data["nodes"], list)
        assert isinstance(data["edges"], list)
    
    def test_graph_nodes_have_required_fields(self):
        """Graph nodes should have id, preset, status, progress, depends_on, dependents"""
        # Create a job first
        job_res = requests.post(f"{API}/jobs", json={"preset": "ARCADE_40"})
        job = job_res.json()
        
        response = requests.get(f"{API}/jobs/graph")
        data = response.json()
        
        # Find our job in nodes
        node = next((n for n in data["nodes"] if n["id"] == job["id"]), None)
        assert node is not None
        assert "id" in node
        assert "preset" in node
        assert "status" in node
        assert "progress" in node
        assert "depends_on" in node
        assert "dependents" in node
        
        # Cleanup
        requests.delete(f"{API}/jobs/{job['id']}")
    
    def test_graph_edges_for_dependencies(self):
        """Graph should have edges for dependencies"""
        # Create parent and child
        parent_res = requests.post(f"{API}/jobs", json={"preset": "ARCADE_40"})
        parent = parent_res.json()
        child_res = requests.post(f"{API}/jobs", json={"preset": "SLOTS_20", "depends_on": [parent["id"]]})
        child = child_res.json()
        
        response = requests.get(f"{API}/jobs/graph")
        data = response.json()
        
        # Should have edge from parent to child
        edge = next((e for e in data["edges"] if e["from"] == parent["id"] and e["to"] == child["id"]), None)
        assert edge is not None, f"Expected edge from {parent['id']} to {child['id']}"
        
        # Cleanup
        requests.delete(f"{API}/jobs/{parent['id']}")
        requests.delete(f"{API}/jobs/{child['id']}")


class TestAutoUnblock:
    """Test auto-unblock when parent job completes"""
    
    def test_blocked_job_unblocks_when_parent_completes(self):
        """Blocked child should transition to pending when parent completes"""
        # Create parent
        parent_res = requests.post(f"{API}/jobs", json={"preset": "ARCADE_40", "priority": "high"})
        parent = parent_res.json()
        parent_id = parent["id"]
        
        # Create blocked child
        child_res = requests.post(f"{API}/jobs", json={
            "preset": "SLOTS_20",
            "depends_on": [parent_id]
        })
        child = child_res.json()
        child_id = child["id"]
        
        # Verify child is blocked
        assert child["status"] == "blocked"
        
        # Wait for parent to complete and child to unblock
        child_unblocked = False
        for _ in range(40):  # Max 120 seconds
            time.sleep(3)
            jobs_res = requests.get(f"{API}/jobs")
            jobs = jobs_res.json().get("jobs", [])
            
            parent_job = next((j for j in jobs if j["id"] == parent_id), None)
            child_job = next((j for j in jobs if j["id"] == child_id), None)
            
            if parent_job and parent_job["status"] == "completed":
                # Parent complete, check child
                if child_job and child_job["status"] in ["pending", "processing", "completed"]:
                    child_unblocked = True
                    break
        
        assert child_unblocked, "Child job should have been unblocked after parent completed"
        
        # Cleanup
        requests.delete(f"{API}/jobs/{parent_id}")
        requests.delete(f"{API}/jobs/{child_id}")


class TestWorkerStatusWithBlocked:
    """Test worker status includes blocked_jobs count"""
    
    def test_worker_status_includes_blocked_count(self):
        """GET /worker/status should include blocked_jobs"""
        response = requests.get(f"{API}/worker/status")
        assert response.status_code == 200
        data = response.json()
        assert "blocked_jobs" in data
        assert isinstance(data["blocked_jobs"], int)
        assert "active_jobs" in data
        assert "completed_jobs" in data
        assert "total_jobs" in data
        assert "running" in data


class TestExistingFeatures:
    """Verify existing features still work"""
    
    def test_game_types_endpoint(self):
        """GET /game-types should work"""
        response = requests.get(f"{API}/game-types")
        assert response.status_code == 200
        assert "game_types" in response.json()
    
    def test_projects_crud(self):
        """Projects CRUD should work"""
        # Create
        create_res = requests.post(f"{API}/projects", json={
            "name": "TEST_Dep_Project",
            "game_type": "fish_shooter",
            "target_platform": "web"
        })
        assert create_res.status_code == 200
        project = create_res.json()
        
        # Read
        get_res = requests.get(f"{API}/projects/{project['id']}")
        assert get_res.status_code == 200
        
        # Delete
        del_res = requests.delete(f"{API}/projects/{project['id']}")
        assert del_res.status_code == 200
    
    def test_builds_endpoint(self):
        """GET /builds should work"""
        response = requests.get(f"{API}/builds")
        assert response.status_code == 200
        assert "builds" in response.json()
    
    def test_compliance_endpoint(self):
        """GET /compliance should work"""
        response = requests.get(f"{API}/compliance")
        assert response.status_code == 200
        assert "reports" in response.json()
    
    def test_deployments_endpoint(self):
        """GET /deployments should work"""
        response = requests.get(f"{API}/deployments")
        assert response.status_code == 200
        assert "deployments" in response.json()
    
    def test_pipelines_endpoint(self):
        """GET /pipelines should work"""
        response = requests.get(f"{API}/pipelines")
        assert response.status_code == 200
        assert "pipelines" in response.json()
    
    def test_tenants_endpoint(self):
        """GET /tenants should work"""
        response = requests.get(f"{API}/tenants")
        assert response.status_code == 200
        assert "tenants" in response.json()
    
    def test_stats_endpoint(self):
        """GET /stats should work"""
        response = requests.get(f"{API}/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total_projects" in data
        assert "supported_game_types" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
