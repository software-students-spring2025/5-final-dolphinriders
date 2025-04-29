// ===== CONFIG =====
const USER_ID = 'u1';  // hardcode or dynamically set after auth

// ===== DOM ELEMENTS =====
// recipe controls
const cookTimeSlider   = document.getElementById('cookTime');
const prepTimeSlider   = document.getElementById('prepTime');
const totalTimeSlider  = document.getElementById('totalTime');
const cookTimeValue    = document.getElementById('cookTimeValue');
const prepTimeValue    = document.getElementById('prepTimeValue');
const totalTimeValue   = document.getElementById('totalTimeValue');

const sortByEl         = document.getElementById('sortBy');
const haveSomeEl       = document.getElementById('haveSome');
const ingredientsEl    = document.getElementById('ingredientsUsed');
const addBtn           = document.getElementById('addIngredient');
const tagListEl        = document.getElementById('tagList');

const resetBtn         = document.getElementById('resetFilters');
const applyBtn         = document.getElementById('applyFilters');

const recipeListEl     = document.getElementById('recipe-list');
const recipeDetailEl   = document.getElementById('recipe-detail');

// pantry controls
const pantryInput      = document.getElementById('pantryInput');
const pantryAdd        = document.getElementById('pantryAdd');
const pantryList       = document.getElementById('pantryList');
const pantrySave       = document.getElementById('pantrySave');

// tabs
const tabs             = document.querySelectorAll('.tab');
const panels           = document.querySelectorAll('.panel');

// ===== TAB SWITCHING =====
tabs.forEach(button => {
  button.addEventListener('click', () => {
    tabs.forEach(t => t.classList.remove('active'));
    button.classList.add('active');

    const panelId = 'panel-' + button.dataset.panel;
    panels.forEach(p => {
      p.classList.toggle('hidden', p.id !== panelId);
    });
  });
});

// ===== SLIDER LABEL UPDATES =====
cookTimeSlider.addEventListener('input', () => {
  cookTimeValue.textContent =
    cookTimeSlider.value === '0' ? 'Any' : cookTimeSlider.value;
});
prepTimeSlider.addEventListener('input', () => {
  prepTimeValue.textContent =
    prepTimeSlider.value === '0' ? 'Any' : prepTimeSlider.value;
});
totalTimeSlider.addEventListener('input', () => {
  totalTimeValue.textContent =
    totalTimeSlider.value === '0' ? 'Any' : totalTimeSlider.value;
});

// ===== TAG MANAGEMENT (Filters) =====
addBtn.addEventListener('click', () => {
  const txt = ingredientsEl.value.trim();
  if (!txt) return;
  const tag = document.createElement('div');
  tag.className = 'tag';
  tag.textContent = txt;
  tag.onclick = () => tag.remove();
  tagListEl.appendChild(tag);
  ingredientsEl.value = '';
});
ingredientsEl.addEventListener('keydown', e => {
  if (e.key === 'Enter') {
    e.preventDefault();
    addBtn.click();
  }
});

// ===== RESET FILTERS =====
resetBtn.addEventListener('click', () => {
  sortByEl.value        = 'percent';
  haveSomeEl.checked    = true;
  cookTimeSlider.value  = 0;
  prepTimeSlider.value  = 0;
  totalTimeSlider.value = 0;
  cookTimeValue.textContent   = 'Any';
  prepTimeValue.textContent   = 'Any';
  totalTimeValue.textContent  = 'Any';
  ingredientsEl.value         = '';
  tagListEl.innerHTML         = '';
  loadRecipes();
});

// ===== APPLY FILTERS =====
applyBtn.addEventListener('click', loadRecipes);

// ===== PANTRY MANAGEMENT =====
function addPantryTag(name) {
  const tag = document.createElement('div');
  tag.className = 'tag';
  tag.textContent = name;
  tag.onclick = () => tag.remove();
  pantryList.appendChild(tag);
}

pantryAdd.addEventListener('click', () => {
  const txt = pantryInput.value.trim();
  if (!txt) return;
  addPantryTag(txt);
  pantryInput.value = '';
});
pantryInput.addEventListener('keydown', e => {
  if (e.key === 'Enter') {
    e.preventDefault();
    pantryAdd.click();
  }
});

pantrySave.addEventListener('click', async () => {
  // collect current tags
  const ingredients = Array.from(pantryList.children)
    .map(tag => tag.textContent);

  // send to server
  const res = await fetch(`/user/${USER_ID}/ingredients`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(ingredients)
  });

  if (!res.ok) {
    alert('Save failed.');
    return;
  }

  // clear and reload from server
  pantryList.innerHTML = '';
  pantryInput.value = '';
  await loadPantry();
  alert('Pantry saved and re-loaded!');
});

async function loadPantry() {
  pantryList.innerHTML = '';
  const res = await fetch(`/user/${USER_ID}/ingredients`);
  if (!res.ok) return;
  const { ingredients } = await res.json();
  ingredients.forEach(addPantryTag);
}

// ===== FETCH & RENDER RECIPES =====
async function loadRecipes() {
  const params = new URLSearchParams({
    sortBy: sortByEl.value,
    timeCook: cookTimeSlider.value,
    prepTime: prepTimeSlider.value,
    totalTime: totalTimeSlider.value,
    haveSome: haveSomeEl.checked
  });
  Array.from(tagListEl.querySelectorAll('.tag'))
    .map(tag => tag.textContent)
    .forEach(ing => params.append('ingredientsUsed', ing));

  recipeListEl.textContent = 'Loading recipes…';
  recipeDetailEl.textContent = 'Click a recipe above to see details.';

  try {
    const res = await fetch(`/recipes?${params.toString()}`);
    if (!res.ok) throw new Error(`Status ${res.status}`);
    const recipes = await res.json();

    if (recipes.length === 0) {
      recipeListEl.textContent = 'No recipes found.';
      return;
    }

    recipeListEl.innerHTML = '';
    recipes.forEach(r => {
      const btn = document.createElement('button');
      btn.textContent   = r.name || `Recipe ${r.id || ''}`;
      btn.className     = 'recipe-item';
      btn.dataset.id    = r.id;
      btn.addEventListener('click', () => loadDetail(r.id));
      recipeListEl.appendChild(btn);
    });

  } catch (err) {
    console.error(err);
    recipeListEl.textContent = 'Failed to load recipes.';
  }
}

async function loadDetail(id) {
  recipeDetailEl.textContent = 'Loading details…';
  try {
    const res = await fetch(`/recipes/${id}`);
    if (!res.ok) {
      recipeDetailEl.textContent = 'Recipe not found.';
      return;
    }
    const r = await res.json();
    recipeDetailEl.innerHTML = `
      <h2>${r.name}</h2>
      <h3>Ingredients</h3>
      <ul>
        ${r.ingredients.map(i =>
          `<li>${i.quantity||''} ${i.unit||''} ${i.name}</li>`
        ).join('')}
      </ul>
      <h3>Instructions</h3>
      <ol>
        ${r.instructions.map(s=>`<li>${s}</li>`).join('')}
      </ol>
    `;
  } catch {
    recipeDetailEl.textContent = 'Could not load recipe details.';
  }
}

// ===== INITIAL LOAD =====
window.addEventListener('DOMContentLoaded', () => {
  loadRecipes();
  loadPantry();
});
