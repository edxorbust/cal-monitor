import { NavLink } from 'react-router-dom';
import { today } from '../../api/tracker';
import './Tracker.css';

export function Page({ title, subtitle, children, date, onDate }) {
  return <main className="tracker">
    <header className="tracker-header"><div><span className="eyebrow">CALORIES / TU DÍA, EN EQUILIBRIO</span><h1>{title}</h1><p>{subtitle}</p></div>
      {onDate && <label className="date-label">Fecha<input aria-label="Fecha" type="date" value={date} max={today()} required onChange={(e) => e.target.value && onDate(e.target.value)} /></label>}
    </header>
    <nav className="tracker-nav" aria-label="Navegación principal">{[['/dashboard','Resumen'],['/food','Comidas'],['/ingredients','Ingredientes'],['/exercises','Actividad'],['/profile','Perfil']].map(([path,label]) => <NavLink key={path} to={path}>{label}</NavLink>)}</nav>
    {children}
  </main>;
}
export function Notice({ children, error = false }) { return children ? <p role={error ? 'alert' : 'status'} className={`notice ${error ? 'error' : ''}`}>{children}</p> : null; }
export function ResourceState({ resource }) {
  return <>{resource.loading && <Notice>Cargando…</Notice>}{resource.error && <Notice error>{resource.error} <button type="button" onClick={resource.reload}>Reintentar</button></Notice>}</>;
}
export function Field({ label, ...props }) {
  return <label className="field">{label}<input {...props} /></label>;
}
export function Empty({ children }) { return <div className="empty">{children}</div>; }
export function Stat({ label, value, unit, tone = '' }) { return <article className={`stat ${tone}`}><span>{label}</span><strong>{value} <small>{unit}</small></strong></article>; }
export function DeleteButton({ onClick, disabled, label = 'Eliminar' }) { return <button type="button" className="text-button danger" disabled={disabled} onClick={() => { if (window.confirm('¿Eliminar este registro?')) onClick(); }}>{label}</button>; }
