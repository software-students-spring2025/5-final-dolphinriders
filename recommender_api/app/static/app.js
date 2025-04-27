// Update slider labels on input
const cookTimeSlider  = document.getElementById('cookTime');
const prepTimeSlider  = document.getElementById('prepTime');
const totalTimeSlider = document.getElementById('totalTime');

cookTimeSlider.addEventListener('input', () => {
  document.getElementById('cookTimeValue').textContent =
    cookTimeSlider.value === '0' ? 'Any' : cookTimeSlider.value;
});
prepTimeSlider.addEventListener('input', () => {
  document.getElementById('prepTimeValue').textContent =
    prepTimeSlider.value === '0' ? 'Any' : prepTimeSlider.value;
});
totalTimeSlider.addEventListener('input', () => {
  document.getElementById('totalTimeValue').textContent =
    totalTimeSlider.value === '0' ? 'Any' : totalTimeSlider.value;
});

// Ingredients tag management
const addBtn = document.getElementById('addIngredient');
const tagListEl = document.getElementById('tagList');

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

// Reset filters
const resetBtn = document.getElementById('resetFilters');
resetBtn.addEventListener('click', () => {
  haveSomeEl.checked   = true;
  sortByEl.value       = 'percent';
  cookTimeSlider.value = 0;
  prepTimeSlider.value = 0;
  totalTimeSlider.value= 0;
  document.getElementById('cookTimeValue').textContent  = 'Any';
  document.getElementById('prepTimeValue').textContent  = 'Any';
  document.getElementById('totalTimeValue').textContent = 'Any';
  ingredientsEl.value     = '';
  tagListEl.innerHTML     = '';
  loadRecipes();
});
