export function SummarySection({ title, items }) {
  return (
    <div className="bg-white rounded shadow p-4">
      <h3 className="font-semibold mb-2">{title}</h3>
      {Array.isArray(items) && items.length > 0 ? (
        <ul className="list-disc pl-5 space-y-1">
          {items.map((item, i) => (
            <li key={i}>{item}</li>
          ))}
        </ul>
      ) : (
        <div className="text-gray-400 italic">Nothing here</div>
      )}
    </div>
  );
}

export function ActionItemsSection({ items }) {
  return (
    <div className="bg-white rounded shadow p-4">
      <h3 className="font-semibold mb-2">Action Items</h3>
      {Array.isArray(items) && items.length > 0 ? (
        <ul className="space-y-1">
          {items.map((item, i) => (
            <li key={i} className="flex items-center gap-2">
              <span>{item.task}</span>
              <span className="text-gray-400 text-sm">({item.owner || "unassigned"})</span>
            </li>
          ))}
        </ul>
      ) : (
        <div className="text-gray-400 italic">Nothing here</div>
      )}
    </div>
  );
}

export function NoiseSection({ noise }) {
  return (
    <div className="bg-white rounded shadow p-4">
      <h3 className="font-semibold mb-2">Everything Else</h3>
      <div className="text-gray-700">{noise ? noise : <span className="text-gray-400 italic">Nothing here</span>}</div>
    </div>
  );
}
