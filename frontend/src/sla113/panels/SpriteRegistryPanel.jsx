import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Image, Plus, XCircle, Play, Layers } from 'lucide-react';

const API_BASE = `${process.env.REACT_APP_BACKEND_URL}/api/sla113`;

const SpriteRegistryPanel = () => {
  const [sprites, setSprites] = useState([]);
  const [selectedSprite, setSelectedSprite] = useState(null);
  const [showRegister, setShowRegister] = useState(false);
  const [filter, setFilter] = useState('all');
  const [form, setForm] = useState({
    name: '', entity_type: 'fish', sprite_url: '',
    frame_width: 256, frame_height: 256, columns: 4, rows: 4, total_frames: 16,
    animations: {}, tier: 0,
  });
  const [animInput, setAnimInput] = useState('');

  useEffect(() => { fetchSprites(); }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const fetchSprites = async () => {
    try {
      const url = filter === 'all' ? `${API_BASE}/sprites` : `${API_BASE}/sprites?entity_type=${filter}`;
      const res = await axios.get(url);
      setSprites(res.data.sprites || []);
    } catch { /* failed */ }
  };

  const registerSprite = async () => {
    if (!form.name || !form.sprite_url) return;
    let anims = {};
    try { anims = animInput ? JSON.parse(animInput) : {}; } catch { /* invalid json */ }
    try {
      await axios.post(`${API_BASE}/sprites/register`, { ...form, animations: anims });
      setShowRegister(false);
      setForm({ name: '', entity_type: 'fish', sprite_url: '', frame_width: 256, frame_height: 256, columns: 4, rows: 4, total_frames: 16, animations: {}, tier: 0 });
      setAnimInput('');
      fetchSprites();
    } catch { /* failed */ }
  };

  const deleteSprite = async (id) => {
    await axios.delete(`${API_BASE}/sprites/${id}`);
    if (selectedSprite?.id === id) setSelectedSprite(null);
    fetchSprites();
  };

  const ENTITY_TYPES = ['fish', 'boss', 'special', 'weapon', 'background', 'ui'];

  return (
    <div className="animate-in fade-in max-w-7xl mx-auto w-full space-y-6" data-testid="sprite-registry-panel">
      <div className="flex items-center justify-between">
        <span className="text-[#D4AF37] text-[10px] font-bold uppercase tracking-[3px] flex items-center gap-2"><Layers size={14}/> Sprite Asset Registry</span>
        <div className="flex gap-2">
          <div className="flex gap-1">
            {['all', ...ENTITY_TYPES].map(t => (
              <button key={t} onClick={() => { setFilter(t); setTimeout(fetchSprites, 0); }}
                className={`px-2 py-1 text-[7px] uppercase tracking-widest border transition-all ${filter === t ? 'border-[#D4AF37] bg-[#D4AF37]/10 text-[#D4AF37]' : 'border-zinc-800 text-zinc-600 hover:text-zinc-300'}`}
              >{t}</button>
            ))}
          </div>
          <button onClick={() => setShowRegister(!showRegister)}
            className={`px-4 py-1.5 border text-[9px] uppercase tracking-widest font-bold transition-all ${showRegister ? 'border-red-500/30 text-red-400' : 'border-[#D4AF37]/30 text-[#D4AF37] hover:bg-[#D4AF37]/10'}`}
            data-testid="register-sprite-btn"
          >{showRegister ? 'Cancel' : 'Register Sprite'}</button>
        </div>
      </div>

      {showRegister && (
        <div className="glass-panel border-[#D4AF37]/20 p-6 space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-[8px] text-zinc-500 uppercase tracking-widest block mb-1">Name</label>
              <input value={form.name} onChange={e => setForm(p => ({...p, name: e.target.value}))} placeholder="Quetzalcoatl Fireborn" className="input-dark focus:border-[#D4AF37]" data-testid="sprite-name" />
            </div>
            <div>
              <label className="text-[8px] text-zinc-500 uppercase tracking-widest block mb-1">Entity Type</label>
              <div className="flex gap-1">
                {ENTITY_TYPES.map(t => (
                  <button key={t} onClick={() => setForm(p => ({...p, entity_type: t}))}
                    className={`flex-1 py-1.5 text-[7px] uppercase tracking-widest border transition-all ${form.entity_type === t ? 'border-[#D4AF37] bg-[#D4AF37]/10 text-[#D4AF37]' : 'border-zinc-800 text-zinc-600'}`}
                  >{t}</button>
                ))}
              </div>
            </div>
          </div>
          <div>
            <label className="text-[8px] text-zinc-500 uppercase tracking-widest block mb-1">Sprite Sheet URL</label>
            <input value={form.sprite_url} onChange={e => setForm(p => ({...p, sprite_url: e.target.value}))} placeholder="https://..." className="input-dark focus:border-[#D4AF37]" data-testid="sprite-url" />
          </div>
          {form.sprite_url && (
            <div className="border border-zinc-800 bg-black/50 p-2 flex justify-center">
              <img src={form.sprite_url} alt="preview" className="max-h-40 object-contain" />
            </div>
          )}
          <div className="grid grid-cols-5 gap-3">
            {[['frame_width', 'Frame W'], ['frame_height', 'Frame H'], ['columns', 'Columns'], ['rows', 'Rows'], ['total_frames', 'Frames']].map(([key, label]) => (
              <div key={key}>
                <label className="text-[7px] text-zinc-500 uppercase tracking-widest block mb-1">{label}</label>
                <input type="number" value={form[key]} onChange={e => setForm(p => ({...p, [key]: parseInt(e.target.value) || 0}))} className="bg-black border border-zinc-800 px-2 py-1.5 text-[10px] text-zinc-200 focus:outline-none focus:border-[#D4AF37] w-full text-center font-mono" />
              </div>
            ))}
          </div>
          <div>
            <label className="text-[8px] text-zinc-500 uppercase tracking-widest block mb-1">Animations (JSON)</label>
            <textarea value={animInput} onChange={e => setAnimInput(e.target.value)} rows={3}
              placeholder='{"idle": [0,1,2,3], "attack": [4,5,6,7], "death": [12,13,14,15]}'
              className="w-full bg-black border border-zinc-800 px-3 py-2 text-[10px] text-zinc-200 focus:outline-none focus:border-[#D4AF37] font-mono resize-none"
            />
          </div>
          <button onClick={registerSprite} disabled={!form.name || !form.sprite_url}
            className="w-full py-3 border border-[#D4AF37] bg-[#D4AF37]/10 text-[#D4AF37] font-bold uppercase text-[10px] tracking-[2px] hover:bg-[#D4AF37] hover:text-black transition-all disabled:opacity-30"
            data-testid="save-sprite-btn"
          >Register Sprite Asset</button>
        </div>
      )}

      <div className="grid grid-cols-12 gap-4">
        <div className="col-span-7 space-y-2 max-h-[500px] overflow-y-auto custom-scrollbar">
          {sprites.length === 0 && <div className="glass-panel border-[#D4AF37]/10 p-12 text-center text-zinc-600 text-[10px] uppercase tracking-widest">No sprites registered. Upload your spritesheets above.</div>}
          {sprites.map(s => (
            <div key={s.id} onClick={() => setSelectedSprite(s)}
              className={`glass-panel p-4 flex items-center gap-4 cursor-pointer transition-all ${selectedSprite?.id === s.id ? 'border-[#D4AF37]/50 bg-[#D4AF37]/5' : 'border-[#D4AF37]/20 hover:border-[#D4AF37]/30'}`}
              data-testid={`sprite-${s.id}`}
            >
              <div className="w-16 h-16 border border-zinc-800 bg-black/50 overflow-hidden flex-shrink-0">
                <img src={s.sprite_url} alt={s.name} className="w-full h-full object-cover" />
              </div>
              <div className="flex-1 min-w-0">
                <h4 className="text-zinc-200 text-xs font-bold truncate">{s.name}</h4>
                <div className="flex gap-3 text-[8px] text-zinc-500 mt-1">
                  <span className="px-1.5 py-0.5 border border-zinc-800 uppercase">{s.entity_type}</span>
                  <span>{s.total_frames} frames</span>
                  <span>{s.frame_width}x{s.frame_height}</span>
                  <span>{s.columns}x{s.rows} grid</span>
                </div>
              </div>
              <button onClick={(e) => { e.stopPropagation(); deleteSprite(s.id); }} className="text-zinc-700 hover:text-red-500"><XCircle size={14}/></button>
            </div>
          ))}
        </div>

        {selectedSprite && (
          <div className="col-span-5 glass-panel border-[#D4AF37]/20 p-6 space-y-4">
            <h3 className="text-[#D4AF37] text-xs font-bold uppercase tracking-widest">{selectedSprite.name}</h3>
            <div className="border border-zinc-800 bg-black overflow-hidden">
              <img src={selectedSprite.sprite_url} alt={selectedSprite.name} className="w-full object-contain" />
            </div>
            <div className="grid grid-cols-2 gap-2 text-[9px]">
              {[
                ['Type', selectedSprite.entity_type],
                ['Frames', selectedSprite.total_frames],
                ['Frame Size', `${selectedSprite.frame_width}x${selectedSprite.frame_height}`],
                ['Grid', `${selectedSprite.columns}x${selectedSprite.rows}`],
                ['Tier', selectedSprite.tier],
                ['ID', selectedSprite.id],
              ].map(([label, val]) => (
                <div key={label} className="bg-black/50 border border-zinc-800 p-2">
                  <div className="text-[7px] text-zinc-600 uppercase tracking-widest">{label}</div>
                  <div className="text-zinc-200 font-mono">{val}</div>
                </div>
              ))}
            </div>
            {selectedSprite.animations && Object.keys(selectedSprite.animations).length > 0 && (
              <div className="space-y-2">
                <span className="text-[8px] text-[#D4AF37] uppercase tracking-widest font-bold">Animations</span>
                {Object.entries(selectedSprite.animations).map(([anim, frames]) => (
                  <div key={anim} className="flex justify-between bg-black/50 border border-zinc-800 p-2">
                    <span className="text-zinc-300 text-[9px] font-mono uppercase">{anim}</span>
                    <span className="text-zinc-500 text-[9px] font-mono">[{frames.join(',')}]</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default SpriteRegistryPanel;
