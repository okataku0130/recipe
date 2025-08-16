import React, { useState, useMemo } from 'react';
import { ChefHat, Plus } from 'lucide-react';
import { RecipeCard } from './components/RecipeCard';
import { SearchBar } from './components/SearchBar';
import { RecipeModal } from './components/RecipeModal';
import { AddRecipeForm } from './components/AddRecipeForm';
import { LoadingSpinner } from './components/LoadingSpinner';
import { ErrorMessage } from './components/ErrorMessage';
import { Recipe, RecipeFormData } from './types/recipe';
import { useRecipes } from './hooks/useRecipes';
import { useCategories } from './hooks/useCategories';

function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('すべて');
  const [selectedRecipe, setSelectedRecipe] = useState<Recipe | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isAddFormOpen, setIsAddFormOpen] = useState(false);

  const { recipes, loading: recipesLoading, error: recipesError, addRecipe, refetch } = useRecipes(searchTerm, selectedCategory);
  const { categories, loading: categoriesLoading, error: categoriesError } = useCategories();

  const handleRecipeClick = (recipe: Recipe) => {
    setSelectedRecipe(recipe);
    setIsModalOpen(true);
  };

  const handleAddRecipe = async (recipeData: RecipeFormData) => {
    try {
      await addRecipe(recipeData);
    } catch (error) {
      console.error('Failed to add recipe:', error);
    }
  };

  if (recipesError || categoriesError) {
    return (
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div className="flex items-center space-x-3">
              <ChefHat className="w-8 h-8 text-orange-600" />
              <h1 className="text-3xl font-bold text-gray-800">美味しいレシピ集</h1>
            </div>
          </div>
        </header>
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <ErrorMessage 
            message={recipesError || categoriesError || 'APIサーバーに接続できません'} 
            onRetry={refetch}
          />
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <ChefHat className="w-8 h-8 text-orange-600" />
              <h1 className="text-3xl font-bold text-gray-800">美味しいレシピ集</h1>
            </div>
            <button
              onClick={() => setIsAddFormOpen(true)}
              className="flex items-center space-x-2 bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded-lg transition-colors"
            >
              <Plus className="w-5 h-5" />
              <span>レシピを追加</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {!categoriesLoading && (
          <SearchBar
            searchTerm={searchTerm}
            onSearchChange={setSearchTerm}
            selectedCategory={selectedCategory}
            onCategoryChange={setSelectedCategory}
            categories={categories}
          />
        )}

        {recipesLoading ? (
          <LoadingSpinner />
        ) : (
          <>
            {/* Results Count */}
            <div className="mb-6">
              <p className="text-gray-600">
                {recipes.length}件のレシピが見つかりました
              </p>
            </div>

            {/* Recipe Grid */}
            {recipes.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {recipes.map((recipe) => (
                  <RecipeCard
                    key={recipe.id}
                    recipe={recipe}
                    onClick={() => handleRecipeClick(recipe)}
                  />
                ))}
              </div>
            ) : (
              <div className="text-center py-12">
                <ChefHat className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                <h3 className="text-xl font-medium text-gray-600 mb-2">
                  レシピが見つかりませんでした
                </h3>
                <p className="text-gray-500">
                  検索条件を変更するか、新しいレシピを追加してみてください。
                </p>
              </div>
            )}
          </>
        )}
      </main>

      {/* Recipe Detail Modal */}
      {selectedRecipe && (
        <RecipeModal
          recipe={selectedRecipe}
          isOpen={isModalOpen}
          onClose={() => {
            setIsModalOpen(false);
            setSelectedRecipe(null);
          }}
        />
      )}

      {/* Add Recipe Form Modal */}
      <AddRecipeForm
        isOpen={isAddFormOpen}
        onClose={() => setIsAddFormOpen(false)}
        onSubmit={handleAddRecipe}
      />
    </div>
  );
}

export default App;