/**
 * Team Settings Page
 * Manage team members and invitations
 */

import { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../context/AuthContext';
import { AdminOnly } from '../components/RoleGate';
import InviteMembersModal from '../components/InviteMembersModal';
import PendingInvitesList from '../components/PendingInvitesList';
import { toast } from 'sonner';

const TeamSettingsPage = () => {
  const { currentTeam, authAxios } = useAuth();
  
  const [members, setMembers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showInviteModal, setShowInviteModal] = useState(false);
  const [inviteRefresh, setInviteRefresh] = useState(0);

  const fetchMembers = useCallback(async () => {
    if (!currentTeam) return;
    
    setLoading(true);
    try {
      const res = await authAxios().get(`/teams/${currentTeam.id}/members`);
      setMembers(res.data);
    } catch (e) {
      console.error('Failed to fetch members:', e);
      setMembers([]);
    } finally {
      setLoading(false);
    }
  }, [authAxios, currentTeam]);

  useEffect(() => {
    fetchMembers();
  }, [fetchMembers]);

  const handleInviteClose = (shouldRefresh) => {
    setShowInviteModal(false);
    if (shouldRefresh) {
      setInviteRefresh(prev => prev + 1);
    }
  };

  const handleRemoveMember = async (userId, email) => {
    if (!window.confirm(`Remove ${email} from the team?`)) {
      return;
    }
    
    try {
      await authAxios().delete(`/teams/${currentTeam.id}/members/${userId}`);
      toast.success(`${email} removed from team`);
      fetchMembers();
    } catch (e) {
      toast.error(e.response?.data?.detail || 'Failed to remove member');
    }
  };

  const handleRoleChange = async (userId, newRole) => {
    try {
      await authAxios().put(`/teams/${currentTeam.id}/members/${userId}/role`, {
        role: newRole,
      });
      toast.success('Role updated');
      fetchMembers();
    } catch (e) {
      toast.error(e.response?.data?.detail || 'Failed to update role');
    }
  };

  const getRoleBadge = (role) => {
    const classes = {
      owner: 'badge-owner',
      admin: 'badge-admin',
      member: 'badge-member',
    };
    return classes[role] || '';
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return 'Unknown';
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  if (!currentTeam) {
    return (
      <div className="page-container" data-testid="team-settings-loading">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="page-container" data-testid="team-settings-page">
      <header className="page-header">
        <h1>Team Settings</h1>
        <p className="subtitle">{currentTeam.name}</p>
      </header>

      <div className="team-settings-grid">
        {/* Members Section */}
        <section className="settings-card members-card" data-testid="members-section">
          <div className="card-header">
            <div>
              <h2>Team Members</h2>
              <span className="member-count">{members.length} members</span>
            </div>
            <AdminOnly>
              <button
                className="btn-primary"
                onClick={() => setShowInviteModal(true)}
                data-testid="invite-btn"
              >
                + Invite Members
              </button>
            </AdminOnly>
          </div>

          {loading ? (
            <div className="members-loading">
              <div className="spinner"></div>
            </div>
          ) : (
            <div className="members-list">
              {members.map((member) => (
                <div key={member.id} className="member-item" data-testid={`member-${member.user_id}`}>
                  <div className="member-info">
                    <div className="member-avatar">
                      {member.first_name?.[0]}{member.last_name?.[0]}
                    </div>
                    <div className="member-details">
                      <span className="member-name">
                        {member.first_name} {member.last_name}
                      </span>
                      <span className="member-email">{member.email}</span>
                    </div>
                  </div>
                  
                  <div className="member-meta">
                    <span className="member-joined">
                      Joined {formatDate(member.joined_at)}
                    </span>
                  </div>
                  
                  <div className="member-actions">
                    {member.role === 'owner' ? (
                      <span className={`role-badge ${getRoleBadge(member.role)}`}>
                        👑 Owner
                      </span>
                    ) : (
                      <AdminOnly
                        fallback={
                          <span className={`role-badge ${getRoleBadge(member.role)}`}>
                            {member.role}
                          </span>
                        }
                      >
                        <select
                          value={member.role}
                          onChange={(e) => handleRoleChange(member.user_id, e.target.value)}
                          className="role-select"
                          data-testid={`role-select-${member.user_id}`}
                        >
                          <option value="member">Member</option>
                          <option value="admin">Admin</option>
                        </select>
                        <button
                          className="btn-remove"
                          onClick={() => handleRemoveMember(member.user_id, member.email)}
                          data-testid={`remove-${member.user_id}`}
                        >
                          Remove
                        </button>
                      </AdminOnly>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>

        {/* Pending Invites Section */}
        <AdminOnly>
          <section className="settings-card invites-card" data-testid="invites-section">
            <div className="card-header">
              <h2>Pending Invitations</h2>
            </div>
            <PendingInvitesList 
              teamId={currentTeam.id} 
              refreshTrigger={inviteRefresh}
            />
          </section>
        </AdminOnly>
      </div>

      {showInviteModal && (
        <InviteMembersModal 
          onClose={handleInviteClose}
          teamId={currentTeam.id}
        />
      )}
    </div>
  );
};

export default TeamSettingsPage;
