'use strict';
const search = document.getElementById('search');
const category = document.getElementById('category');
const cards = [...document.querySelectorAll('.project')];
function filterProjects() {
  const terms = search.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
  let visible = 0;
  for (const card of cards) {
    const matches = (!category.value || card.dataset.category === category.value)
      && terms.every(term => card.dataset.search.includes(term));
    card.hidden = !matches;
    if (matches) visible += 1;
  }
  document.getElementById('count').textContent = `${visible} of ${cards.length} projects`;
  document.getElementById('empty').hidden = visible !== 0;
}
search.addEventListener('input', filterProjects);
category.addEventListener('change', filterProjects);
document.getElementById('reset').addEventListener('click', () => {
  search.value = '';
  category.value = '';
  filterProjects();
  search.focus();
});
