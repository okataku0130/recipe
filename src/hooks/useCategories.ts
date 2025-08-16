import { useState, useEffect } from 'react';
import { apiService } from '../services/api';

export const useCategories = () => {
  const [categories, setCategories] = useState<string[]>(['すべて']);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await apiService.getCategories();
        setCategories(response.categories);
      } catch (err) {
        setError('カテゴリーの取得に失敗しました');
        console.error('Failed to fetch categories:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchCategories();
  }, []);

  return { categories, loading, error };
};