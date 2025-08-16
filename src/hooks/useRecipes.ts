import { useState, useEffect } from 'react';
import { Recipe } from '../types/recipe';
import { apiService } from '../services/api';

export const useRecipes = (searchTerm: string, selectedCategory: string) => {
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchRecipes = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiService.getRecipes(searchTerm, selectedCategory);
      setRecipes(response.recipes);
    } catch (err) {
      setError('レシピの取得に失敗しました');
      console.error('Failed to fetch recipes:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecipes();
  }, [searchTerm, selectedCategory]);

  const addRecipe = async (recipeData: any) => {
    try {
      const newRecipe = await apiService.createRecipe(recipeData);
      setRecipes(prev => [newRecipe, ...prev]);
      return newRecipe;
    } catch (err) {
      setError('レシピの追加に失敗しました');
      throw err;
    }
  };

  return {
    recipes,
    loading,
    error,
    addRecipe,
    refetch: fetchRecipes
  };
};