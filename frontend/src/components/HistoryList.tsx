type Item = { id:number; text:string; emotion:string; created_at:string; };

export default function HistoryList({ items }:{items: Item[]}) {
  if (!items?.length) return null;
  return (
    <div className="rounded-2xl shadow p-4 bg-white/80">
      <div className="text-lg font-semibold mb-2">Your recent moods</div>
      <ul className="space-y-2">
        {items.map(it=>(
          <li key={it.id} className="flex justify-between text-sm">
            <span className="truncate max-w-[70%]">"{it.text}"</span>
            <span className="capitalize opacity-70">{it.emotion}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
