// recommender_api/app/static/app.js

const listEl   = document.getElementById('recipe-list');
const detailEl = document.getElementById('recipe-detail');

// 1) Fetch & render recipe list
function loadRecipes() {
  listEl.textContent = 'Loading recipes…';
  fetch('/recipes')
    .then(res => res.json())
    .then(recipes => {
      listEl.innerHTML = '';
      if (!recipes.length) {
        listEl.textContent = 'No recipes found.';
        return;
      }
      recipes.forEach(r => {
        // r may be an object with {id, name} or just an ID
        const id   = r.id || r;
        const name = r.name || `Recipe ${id}`;
        const btn  = document.createElement('button');
        btn.textContent = name;
        btn.onclick = () => loadDetail(id, name);
        listEl.appendChild(btn);
      });
    })
    .catch(() => {
      listEl.textContent = 'Failed to load recipes.';
    });
}

// 2) Fetch & render a single recipe detail
function loadDetail(id, defaultName = '') {
  detailEl.textContent = 'Loading details…';
  fetch(`/recipes/${id}`)
    .then(res => {
      if (!res.ok) throw new Error();
      return res.json();
    })
    .then(r => {
      detailEl.innerHTML = `
        <h2>${r.name || defaultName}</h2>
        <h3>Ingredients</h3>
        <ul>
          ${r.ingredients.map(i =>
            `<li>${i.quantity || ''} ${i.unit || ''} ${i.name}</li>`
          ).join('')}
        </ul>
        <h3>Instructions</h3>
        <ol>
          ${r.instructions.map(step => `<li>${step}</li>`).join('')}
        </ol>
      `;
    })
    .catch(() => {
      detailEl.textContent = 'Could not load recipe details.';
    });
}

// Start the app
loadRecipes();
