// State Management
let recipes = [];
let allIngredients = [];

const state = {
    includedIngredients: [],
    excludedIngredients: [],
    selectedPresets: new Set(),
    selectedProteinTypes: new Set(),
    selectedMeal: null,
    selectedTime: null,
    recipeSearchQuery: '',
    fuzzyMatch: true
};

const popularIngredientsList = ["חזה עוף", "פילה סלמון", "ברוקולי", "עגבניות", "בטטה", "ביצים", "פסטה", "טופו", "עדשים כתומות", "פטריות"];

// DOM Elements
const elements = {
    recipeGrid: document.getElementById('recipes-grid'),
    emptyState: document.getElementById('empty-state'),
    recipeSearch: document.getElementById('recipe-search'),
    ingredientSearch: document.getElementById('ingredient-search'),
    searchSuggestions: document.getElementById('search-suggestions'),
    includeTags: document.getElementById('include-tags'),
    excludeTags: document.getElementById('exclude-tags'),
    popularIngredients: document.getElementById('popular-ingredients'),
    fuzzyMatchToggle: document.getElementById('fuzzy-match-toggle'),
    recipesCountText: document.getElementById('recipes-count-text'),
    clearFiltersBtn: document.getElementById('clear-filters-btn'),
    emptyResetBtn: document.getElementById('empty-reset-btn'),
    recipeModal: document.getElementById('recipe-modal'),
    closeModalBtn: document.getElementById('close-modal-btn'),
    modalBodyContent: document.getElementById('modal-body-content')
};

// Initialize Application
document.addEventListener('DOMContentLoaded', () => {
    fetchRecipes();
    setupEventListeners();
});

// Fetch Recipes from Database
async function fetchRecipes() {
    try {
        const response = await fetch('src/data/recipes.json');
        if (!response.ok) {
            throw new Error('שגיאה בטעינת מאגר המתכונים');
        }
        recipes = await response.json();
        
        // Extract all unique ingredients from recipes
        const ingredientsSet = new Set();
        recipes.forEach(recipe => {
            recipe.matchableIngredients.forEach(ing => {
                ingredientsSet.add(ing.trim());
            });
        });
        allIngredients = Array.from(ingredientsSet).sort();
        
        // Render Initial UI
        renderPopularIngredients();
        filterAndRenderRecipes();
        
        // Initialise Lucide icons
        lucide.createIcons();
    } catch (error) {
        console.error('Error fetching recipes:', error);
        elements.recipeGrid.innerHTML = `
            <div class="empty-state glass">
                <i data-lucide="alert-triangle" style="color: var(--accent-red); width: 48px; height: 48px;"></i>
                <h2>שגיאה בטעינת הנתונים</h2>
                <p>לא הצלחנו לטעון את המתכונים. אנא נסה לרענן את העמוד.</p>
            </div>
        `;
        lucide.createIcons();
    }
}

// Setup Event Listeners
function setupEventListeners() {
    // Recipe text search
    elements.recipeSearch.addEventListener('input', (e) => {
        state.recipeSearchQuery = e.target.value.trim();
        filterAndRenderRecipes();
    });
    
    // Ingredient search input (autocomplete)
    elements.ingredientSearch.addEventListener('input', handleIngredientSearchInput);
    elements.ingredientSearch.addEventListener('focus', handleIngredientSearchInput);
    
    // Close suggestions box when clicking outside
    document.addEventListener('click', (e) => {
        if (!elements.ingredientSearch.contains(e.target) && !elements.searchSuggestions.contains(e.target)) {
            elements.searchSuggestions.classList.add('hidden');
        }
    });
    
    // Fuzzy match checkbox
    elements.fuzzyMatchToggle.addEventListener('change', (e) => {
        state.fuzzyMatch = e.target.checked;
        filterAndRenderRecipes();
    });
    
    // Preset Filters (high protein, etc.)
    document.querySelectorAll('.preset-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const preset = btn.dataset.preset;
            if (state.selectedPresets.has(preset)) {
                state.selectedPresets.delete(preset);
                btn.classList.remove('active');
            } else {
                state.selectedPresets.add(preset);
                btn.classList.add('active');
            }
            filterAndRenderRecipes();
        });
    });
    
    // Protein Type Filters
    document.querySelectorAll('.protein-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const protein = btn.dataset.protein;
            if (state.selectedProteinTypes.has(protein)) {
                state.selectedProteinTypes.delete(protein);
                btn.classList.remove('active');
            } else {
                state.selectedProteinTypes.add(protein);
                btn.classList.add('active');
            }
            filterAndRenderRecipes();
        });
    });
    
    // Meal Filters
    document.querySelectorAll('.meal-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const meal = btn.dataset.meal;
            if (state.selectedMeal === meal) {
                state.selectedMeal = null;
                btn.classList.remove('active');
            } else {
                document.querySelectorAll('.meal-btn').forEach(b => b.classList.remove('active'));
                state.selectedMeal = meal;
                btn.classList.add('active');
            }
            filterAndRenderRecipes();
        });
    });
    
    // Time Filters
    document.querySelectorAll('.time-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const time = btn.dataset.time;
            if (state.selectedTime === time) {
                state.selectedTime = null;
                btn.classList.remove('active');
            } else {
                document.querySelectorAll('.time-btn').forEach(b => b.classList.remove('active'));
                state.selectedTime = time;
                btn.classList.add('active');
            }
            filterAndRenderRecipes();
        });
    });
    
    // Clear Filters Buttons
    elements.clearFiltersBtn.addEventListener('click', resetAllFilters);
    elements.emptyResetBtn.addEventListener('click', resetAllFilters);
    
    // Modal events
    elements.closeModalBtn.addEventListener('click', closeModal);
    elements.recipeModal.addEventListener('click', (e) => {
        if (e.target === elements.recipeModal) closeModal();
    });
    
    // Close modal on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && !elements.recipeModal.classList.contains('hidden')) {
            closeModal();
        }
    });
}

// Autocomplete logic for ingredients
function handleIngredientSearchInput(e) {
    const query = e.target.value.trim().toLowerCase();
    
    // If input is empty, show all available ingredients that aren't selected yet
    const filtered = allIngredients.filter(ing => {
        const isSelected = state.includedIngredients.includes(ing) || state.excludedIngredients.includes(ing);
        if (isSelected) return false;
        if (query === '') return popularIngredientsList.includes(ing); // Show popular ones when search empty
        return ing.toLowerCase().includes(query);
    });
    
    renderSuggestions(filtered);
}

function renderSuggestions(suggestions) {
    if (suggestions.length === 0) {
        elements.searchSuggestions.classList.add('hidden');
        return;
    }
    
    elements.searchSuggestions.innerHTML = '';
    suggestions.forEach(ing => {
        const div = document.createElement('div');
        div.className = 'suggestion-item';
        
        const nameSpan = document.createElement('span');
        nameSpan.textContent = ing;
        
        const actionsDiv = document.createElement('div');
        actionsDiv.className = 'actions';
        actionsDiv.style.display = 'flex';
        actionsDiv.style.gap = '0.5rem';
        
        // Include button (+)
        const incBtn = document.createElement('button');
        incBtn.className = 'suggestion-action';
        incBtn.style.color = 'var(--accent-green)';
        incBtn.innerHTML = '+ הכלל';
        incBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            addIncludeIngredient(ing);
            elements.ingredientSearch.value = '';
            elements.searchSuggestions.classList.add('hidden');
        });
        
        // Exclude button (-)
        const excBtn = document.createElement('button');
        excBtn.className = 'suggestion-action';
        excBtn.style.color = 'var(--accent-red)';
        excBtn.innerHTML = '- הוצא';
        excBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            addExcludeIngredient(ing);
            elements.ingredientSearch.value = '';
            elements.searchSuggestions.classList.add('hidden');
        });
        
        actionsDiv.appendChild(incBtn);
        actionsDiv.appendChild(excBtn);
        div.appendChild(nameSpan);
        div.appendChild(actionsDiv);
        
        // Clicking row directly adds to Include by default
        div.addEventListener('click', () => {
            addIncludeIngredient(ing);
            elements.ingredientSearch.value = '';
            elements.searchSuggestions.classList.add('hidden');
        });
        
        elements.searchSuggestions.appendChild(div);
    });
    
    elements.searchSuggestions.classList.remove('hidden');
}

// Add/Remove Tags
function addIncludeIngredient(ing) {
    if (state.includedIngredients.includes(ing)) return;
    if (state.excludedIngredients.includes(ing)) {
        // Remove from excluded first
        state.excludedIngredients = state.excludedIngredients.filter(item => item !== ing);
    }
    
    // Check limit of 5 inclusion ingredients
    if (state.includedIngredients.length >= 5) {
        alert('ניתן לסמן עד 5 רכיבים להכללה בלבד.');
        return;
    }
    
    state.includedIngredients.push(ing);
    renderTags();
    renderPopularIngredients();
    filterAndRenderRecipes();
}

function addExcludeIngredient(ing) {
    if (state.excludedIngredients.includes(ing)) return;
    if (state.includedIngredients.includes(ing)) {
        // Remove from included first
        state.includedIngredients = state.includedIngredients.filter(item => item !== ing);
    }
    
    state.excludedIngredients.push(ing);
    renderTags();
    renderPopularIngredients();
    filterAndRenderRecipes();
}

function removeIncludeIngredient(ing) {
    state.includedIngredients = state.includedIngredients.filter(item => item !== ing);
    renderTags();
    renderPopularIngredients();
    filterAndRenderRecipes();
}

function removeExcludeIngredient(ing) {
    state.excludedIngredients = state.excludedIngredients.filter(item => item !== ing);
    renderTags();
    renderPopularIngredients();
    filterAndRenderRecipes();
}

// Render selected tag badges
function renderTags() {
    elements.includeTags.innerHTML = '';
    state.includedIngredients.forEach(ing => {
        const span = document.createElement('span');
        span.className = 'ingredient-tag include';
        span.innerHTML = `
            ${ing}
            <button onclick="event.stopPropagation(); removeIncludeIngredient('${ing}')">×</button>
        `;
        elements.includeTags.appendChild(span);
    });
    
    elements.excludeTags.innerHTML = '';
    state.excludedIngredients.forEach(ing => {
        const span = document.createElement('span');
        span.className = 'ingredient-tag exclude';
        span.innerHTML = `
            ${ing}
            <button onclick="event.stopPropagation(); removeExcludeIngredient('${ing}')">×</button>
        `;
        elements.excludeTags.appendChild(span);
    });
}

// Render popular ingredients section
function renderPopularIngredients() {
    elements.popularIngredients.innerHTML = '';
    popularIngredientsList.forEach(ing => {
        const isIncluded = state.includedIngredients.includes(ing);
        const isExcluded = state.excludedIngredients.includes(ing);
        
        const badge = document.createElement('span');
        badge.className = 'popular-badge';
        if (isIncluded) {
            badge.className += ' active-include';
        } else if (isExcluded) {
            badge.style.background = 'rgba(224, 62, 82, 0.15)';
            badge.style.borderColor = 'var(--accent-red)';
            badge.style.color = '#fca5a5';
        }
        badge.textContent = ing;
        
        badge.addEventListener('click', () => {
            if (isIncluded) {
                removeIncludeIngredient(ing);
            } else if (isExcluded) {
                removeExcludeIngredient(ing);
            } else {
                addIncludeIngredient(ing);
            }
        });
        
        elements.popularIngredients.appendChild(badge);
    });
}

// Reset all filters
function resetAllFilters() {
    state.includedIngredients = [];
    state.excludedIngredients = [];
    state.selectedPresets.clear();
    state.selectedProteinTypes.clear();
    state.selectedMeal = null;
    state.selectedTime = null;
    state.recipeSearchQuery = '';
    
    // Reset inputs & buttons class lists
    elements.recipeSearch.value = '';
    elements.ingredientSearch.value = '';
    elements.fuzzyMatchToggle.checked = true;
    state.fuzzyMatch = true;
    
    document.querySelectorAll('.preset-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.protein-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.meal-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.time-btn').forEach(btn => btn.classList.remove('active'));
    
    renderTags();
    renderPopularIngredients();
    filterAndRenderRecipes();
}

// Fuzzy Matching & Filter Logic Core
function filterAndRenderRecipes() {
    const filtered = recipes.map(recipe => {
        let matchScore = 100;
        let matchedCount = 0;
        
        // 1. Exclude Filter: If it contains any excluded ingredients, filter out completely (score = 0)
        const containsExcluded = recipe.matchableIngredients.some(ing => 
            state.excludedIngredients.includes(ing)
        );
        if (containsExcluded) {
            return { ...recipe, score: 0, isFilteredOut: true };
        }
        
        // 2. Text Search Query Filter with Hebrew-aware fuzzy word matching
        if (state.recipeSearchQuery !== '') {
            const query = state.recipeSearchQuery.toLowerCase().trim();
            const queryWords = query.split(/\s+/).filter(w => w.length > 0);
            const recipeText = `${recipe.name} ${recipe.description} ${recipe.tags.join(' ')}`.toLowerCase();
            
            // Helper to check if a single query word matches any part of the recipe text with Hebrew prefix/stem flexibility
            const isWordMatched = (qWord) => {
                if (recipeText.includes(qWord)) return true;
                
                // Clean non-alphanumeric (like brackets or punctuation)
                const qWordClean = qWord.replace(/[^\u0590-\u05fe\w]/g, '');
                if (qWordClean.length < 3) return false;
                
                // Extract words from recipe text and check for similarities
                const words = recipeText.split(/[^\u0590-\u05fe\w]+/).filter(w => w.length > 0);
                for (const w of words) {
                    if (w.includes(qWordClean) || qWordClean.includes(w)) return true;
                    // Common root prefix match (e.g. sharing first 4 letters for long words)
                    if (w.length >= 4 && qWordClean.length >= 4) {
                        if (w.substring(0, 4) === qWordClean.substring(0, 4)) return true;
                    }
                }
                return false;
            };
            
            // A recipe matches if ALL query words are matched in any order
            const allWordsMatched = queryWords.every(word => isWordMatched(word));
            if (!allWordsMatched) {
                return { ...recipe, score: 0, isFilteredOut: true };
            }
        }
        
        // 3. Meal Category Filter
        if (state.selectedMeal) {
            const categories = recipe.category.split(',').map(c => c.trim());
            if (!categories.includes(state.selectedMeal)) {
                return { ...recipe, score: 0, isFilteredOut: true };
            }
        }
        
        // 3b. Protein Type Filter
        if (state.selectedProteinTypes.size > 0) {
            if (!state.selectedProteinTypes.has(recipe.proteinType)) {
                return { ...recipe, score: 0, isFilteredOut: true };
            }
        }
        
        // 4. Cooking Time Filter
        if (state.selectedTime) {
            if (state.selectedTime === 'quick' && recipe.totalTime > 30) {
                return { ...recipe, score: 0, isFilteredOut: true };
            }
            if (state.selectedTime === 'medium' && (recipe.totalTime <= 30 || recipe.totalTime > 60)) {
                return { ...recipe, score: 0, isFilteredOut: true };
            }
            if (state.selectedTime === 'slow' && recipe.totalTime <= 60) {
                return { ...recipe, score: 0, isFilteredOut: true };
            }
        }
        
        // 5. Nutrient / Diet Presets Filter
        if (state.selectedPresets.size > 0) {
            let presetPass = true;
            if (state.selectedPresets.has('high-protein') && recipe.protein < 30) presetPass = false;
            if (state.selectedPresets.has('low-carb') && recipe.carbs > 20) presetPass = false;
            if (state.selectedPresets.has('low-calorie') && recipe.calories > 400) presetPass = false;
            if (state.selectedPresets.has('vegan') && !recipe.tags.includes('טבעוני')) presetPass = false;
            
            if (!presetPass) {
                return { ...recipe, score: 0, isFilteredOut: true };
            }
        }
        
        // 6. Fuzzy Match Score calculation based on Inclusion list
        if (state.includedIngredients.length > 0) {
            state.includedIngredients.forEach(ing => {
                if (recipe.matchableIngredients.includes(ing)) {
                    matchedCount++;
                }
            });
            matchScore = Math.round((matchedCount / state.includedIngredients.length) * 100);
            
            // Filter out if it doesn't satisfy fuzzy/strict criteria
            if (state.fuzzyMatch) {
                // Fuzzy: must match at least 50%
                if (matchScore < 50) {
                    return { ...recipe, score: matchScore, isFilteredOut: true };
                }
            } else {
                // Strict: must match 100%
                if (matchScore < 100) {
                    return { ...recipe, score: matchScore, isFilteredOut: true };
                }
            }
        }
        
        return { ...recipe, score: matchScore, isFilteredOut: false };
    }).filter(recipe => !recipe.isFilteredOut);
    
    // Sort by match score descending, then by total time ascending
    filtered.sort((a, b) => {
        if (b.score !== a.score) {
            return b.score - a.score;
        }
        return a.totalTime - b.totalTime;
    });
    
    renderRecipesList(filtered);
}

// Render recipe card grid
function renderRecipesList(filteredRecipes) {
    elements.recipeGrid.innerHTML = '';
    elements.recipesCountText.textContent = `נמצאו ${filteredRecipes.length} מתכונים`;
    
    if (filteredRecipes.length === 0) {
        elements.emptyState.classList.remove('hidden');
        elements.recipeGrid.appendChild(elements.emptyState);
        return;
    }
    
    elements.emptyState.classList.add('hidden');
    
    filteredRecipes.forEach(recipe => {
        const card = document.createElement('div');
        card.className = 'recipe-card glass';
        
        // Determine match percentage class
        let badgeClass = 'perfect';
        let badgeIcon = 'check';
        if (recipe.score < 100) {
            badgeClass = 'partial';
            badgeIcon = 'alert-circle';
        }
        
        card.innerHTML = `
            <div class="card-image-wrapper">
                <img src="${recipe.image}" alt="${recipe.name}">
                <div class="card-image-overlay">
                    <span class="card-time-badge">
                        <i data-lucide="clock" style="width:12px; height:12px;"></i>
                        ${recipe.totalTime} דק'
                    </span>
                </div>
                ${state.includedIngredients.length > 0 ? `
                    <span class="match-badge ${badgeClass}">
                        <i data-lucide="${badgeIcon}" style="width:12px; height:12px;"></i>
                        ${recipe.score}% התאמה
                    </span>
                ` : ''}
            </div>
            <div class="card-content">
                <h2 class="card-title">${recipe.name}</h2>
                <p class="card-description">${recipe.description}</p>
                <div class="card-macros">
                    <div class="macro-box calories">
                        <span class="macro-val">${recipe.calories}</span>
                        <span class="macro-label">קלוריות</span>
                    </div>
                    <div class="macro-box protein">
                        <span class="macro-val">${recipe.protein}ג</span>
                        <span class="macro-label">חלבון</span>
                    </div>
                    <div class="macro-box carbs">
                        <span class="macro-val">${recipe.carbs}ג</span>
                        <span class="macro-label">פחמימה</span>
                    </div>
                    <div class="macro-box fat">
                        <span class="macro-val">${recipe.fat}ג</span>
                        <span class="macro-label">שומן</span>
                    </div>
                </div>
            </div>
        `;
        
        card.addEventListener('click', () => openRecipeDetails(recipe));
        elements.recipeGrid.appendChild(card);
    });
    
    // Refresh icons inside cards
    lucide.createIcons();
}

// Recipe detail modal variables
let currentPortions = 2;
let activeRecipe = null;

// Open recipe details modal
function openRecipeDetails(recipe) {
    activeRecipe = recipe;
    currentPortions = recipe.portions;
    
    renderModalContent();
    elements.recipeModal.classList.remove('hidden');
    document.body.style.overflow = 'hidden'; // Lock screen scroll
}

function closeModal() {
    elements.recipeModal.classList.add('hidden');
    document.body.style.overflow = 'auto'; // Restore screen scroll
    activeRecipe = null;
}

// Dynamic Portion Scaling & Recipe Modal Details Renderer
function renderModalContent() {
    if (!activeRecipe) return;
    
    // Generate ingredients rows with scaled portions
    let ingredientsHTML = '';
    activeRecipe.ingredients.forEach((ing, index) => {
        // Portion scaling math
        let amount = parseFloat(ing.amount);
        let displayAmount = '';
        if (!isNaN(amount)) {
            let scaledAmount = (amount * currentPortions) / activeRecipe.portions;
            // Round to 1 decimal place if floating, or keep integer
            displayAmount = Number(scaledAmount.toFixed(1)).toString();
        } else {
            displayAmount = ing.amount; // Textual amount like "לפי טעם"
        }
        
        ingredientsHTML += `
            <label class="ingredient-item" id="ing-item-${index}">
                <input type="checkbox" onchange="toggleIngredientCheck(${index})">
                <span class="checkbox-custom"></span>
                <div class="ingredient-details">
                    <span class="ingredient-name" id="ing-name-${index}">${ing.name}</span>
                    <span class="ingredient-qty">${displayAmount} ${ing.unit}</span>
                </div>
            </label>
        `;
    });
    
    // Generate step by step instructions checklist
    let stepsHTML = '';
    activeRecipe.instructions.forEach((step, index) => {
        stepsHTML += `
            <div class="step-item" id="step-item-${index}" onclick="toggleStepCheck(${index})">
                <div class="step-num">${index + 1}</div>
                <div class="step-text" id="step-text-${index}">${step}</div>
            </div>
        `;
    });
    
    // Generate tags badges
    let tagsHTML = '';
    activeRecipe.tags.forEach(tag => {
        tagsHTML += `<span class="recipe-badge highlight">${tag}</span>`;
    });
    
    // Scale macro numbers based on portions
    // Note: Database macros are defined PER PORTION, so they don't scale with portions size change.
    // They are constant values representing the nutritional content of a single serving.
    
    elements.modalBodyContent.innerHTML = `
        <!-- Left Side: Image and Nutrition -->
        <div class="modal-left">
            <div class="modal-img-container">
                <img src="${activeRecipe.image}" alt="${activeRecipe.name}">
            </div>
            
            <div class="modal-nutrition-wrapper">
                <h3 class="modal-macros-title"><i data-lucide="info" style="display:inline; width:16px; height:16px; vertical-align:middle;"></i> ערכים תזונתיים (למנה בודדת)</h3>
                <div class="modal-macros-grid">
                    <div class="modal-macro-card calories">
                        <span class="val">${activeRecipe.calories}</span>
                        <span class="lbl">קלוריות</span>
                    </div>
                    <div class="modal-macro-card protein">
                        <span class="val">${activeRecipe.protein}ג</span>
                        <span class="lbl">חלבון</span>
                    </div>
                    <div class="modal-macro-card carbs">
                        <span class="val">${activeRecipe.carbs}ג</span>
                        <span class="lbl">פחמימות</span>
                    </div>
                    <div class="modal-macro-card fat">
                        <span class="val">${activeRecipe.fat}ג</span>
                        <span class="lbl">שומן</span>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Right Side: Details and Steps -->
        <div class="modal-right">
            <div class="recipe-header-info">
                <h2>${activeRecipe.name}</h2>
                <div class="recipe-badges">
                    <span class="recipe-badge"><i data-lucide="clock" style="width:14px; height:14px;"></i> הכנה: ${activeRecipe.totalTime} דק'</span>
                    <span class="recipe-badge"><i data-lucide="activity" style="width:14px; height:14px;"></i> רמת קושי: ${activeRecipe.difficulty}</span>
                    <span class="recipe-badge"><i data-lucide="layers" style="width:14px; height:14px;"></i> ארוחה: ${activeRecipe.category}</span>
                    ${tagsHTML}
                </div>
            </div>
            
            <p class="recipe-desc">${activeRecipe.description}</p>
            
            <!-- Portions Changer -->
            <div class="portions-selector-wrapper">
                <span class="portions-title">כמות מנות לחישוב:</span>
                <div class="portions-controls">
                    <button class="portions-btn" onclick="updatePortions(-1)">-</button>
                    <span class="portions-num" id="portions-display-num">${currentPortions}</span>
                    <button class="portions-btn" onclick="updatePortions(1)">+</button>
                </div>
            </div>
            
            <!-- Ingredients Checklist -->
            <div class="ingredients-list-wrapper">
                <h4><i data-lucide="shopping-cart"></i> מצרכים נדרשים:</h4>
                <div class="ingredients-checklist">
                    ${ingredientsHTML}
                </div>
            </div>
            
            <!-- Instructions Checklist -->
            <div class="instructions-list-wrapper">
                <h4><i data-lucide="chef-hat"></i> שלבי הכנה:</h4>
                <div class="instructions-checklist">
                    ${stepsHTML}
                </div>
            </div>
        </div>
    `;
    
    // Initialize icons in modal
    lucide.createIcons();
}

// Global hook helpers for onclick events inside modal template
window.updatePortions = function(change) {
    const newPortions = currentPortions + change;
    if (newPortions < 1 || newPortions > 20) return;
    currentPortions = newPortions;
    
    // Redraw portions display
    document.getElementById('portions-display-num').textContent = currentPortions;
    
    // Recalculate and update ingredients checklist amount fields dynamically
    activeRecipe.ingredients.forEach((ing, index) => {
        const amount = parseFloat(ing.amount);
        if (!isNaN(amount)) {
            const scaledAmount = (amount * currentPortions) / activeRecipe.portions;
            const displayAmount = Number(scaledAmount.toFixed(1)).toString();
            // Find target element and update text
            const label = document.getElementById(`ing-item-${index}`);
            if (label) {
                const qtySpan = label.querySelector('.ingredient-qty');
                if (qtySpan) {
                    qtySpan.textContent = `${displayAmount} ${ing.unit}`;
                }
            }
        }
    });
};

window.toggleIngredientCheck = function(index) {
    const item = document.getElementById(`ing-item-${index}`);
    const checkbox = item.querySelector('input[type="checkbox"]');
    if (checkbox.checked) {
        item.style.opacity = '0.6';
    } else {
        item.style.opacity = '1';
    }
};

window.toggleStepCheck = function(index) {
    const step = document.getElementById(`step-item-${index}`);
    step.classList.toggle('completed');
};

// Expose tag removal functions to window context for onclick tags
window.removeIncludeIngredient = removeIncludeIngredient;
window.removeExcludeIngredient = removeExcludeIngredient;
