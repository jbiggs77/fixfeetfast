/* Progressive enhancement: all discussions and pagination work without JavaScript. */
(() => {
  const form = document.querySelector('[data-archive-search]');
  if (!form) return;
  const input = form.querySelector('input[name="q"]');
  const state = document.querySelector('[data-state-filter]');
  const results = document.querySelector('[data-search-results]');
  const original = document.querySelector('[data-browse-results]');
  const status = document.querySelector('[data-search-status]');
  let records;
  let generation = 0;
  const node = (tag, text, className) => {
    const el = document.createElement(tag);
    if (text !== undefined) el.textContent = text;
    if (className) el.className = className;
    return el;
  };
  const render = async () => {
    const current = ++generation;
    const query = input.value.trim();
    const selected = state ? state.value : '';
    const params = new URLSearchParams();
    if (query) params.set('q', query);
    if (selected) params.set('state', selected);
    history.replaceState(null, '', location.pathname + (params.size ? '?' + params : ''));
    if (!query && !selected) {
      results.replaceChildren(); original.hidden = false; status.textContent = ''; return;
    }
    status.textContent = 'Searching the discussion archive…';
    try {
      if (!records) {
        const response = await fetch(form.dataset.archiveSearch);
        if (!response.ok) throw new Error('Search unavailable');
        records = await response.json();
      }
      if (current !== generation) return;
      const terms = query.toLocaleLowerCase().split(/\s+/).filter(Boolean);
      const matches = records.filter(row => (!selected || row.states.includes(selected)) &&
        terms.every(term => row.search.includes(term)));
      const fragment = document.createDocumentFragment();
      for (const row of matches.slice(0, 60)) {
        const article = node('article', undefined, 'discussion-row');
        const heading = node('h3'); const link = node('a', row.title); link.href = row.url;
        heading.append(link); article.append(heading, node('p', row.excerpt));
        const meta = node('div', `${row.replies} archived replies`, 'row-meta');
        if (row.topic) meta.append(node('span', row.topic, 'category'));
        article.append(meta); fragment.append(article);
      }
      if (!matches.length) fragment.append(node('p', 'No matching discussions. Try a broader risk, carrier or state.', 'no-results'));
      results.replaceChildren(fragment); original.hidden = true;
      status.textContent = `${matches.length.toLocaleString()} matching discussions` +
        (matches.length > 60 ? '. Showing the first 60; narrow your search for more specific results.' : '.');
    } catch (_) {
      status.textContent = 'Search is temporarily unavailable. You can still browse every discussion below.';
      original.hidden = false;
    }
  };
  const params = new URLSearchParams(location.search);
  input.value = params.get('q') || '';
  if (state) state.value = params.get('state') || '';
  form.addEventListener('submit', event => { event.preventDefault(); render(); });
  if (state) state.addEventListener('change', render);
  if (input.value || (state && state.value)) render();
})();
