const API_BASE_URL = 'http://localhost:8080/api';

export interface ApiResponse<T> {
  data: T;
  error?: string;
}

export interface RecipesResponse {
  recipes: any[];
  total: number;
}

export interface CategoriesResponse {
  categories: string[];
}

export interface ImageResponse {
  image_url: string;
}

export interface ImagesResponse {
  images: string[];
}

class ApiService {
  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  async getRecipes(searchTerm?: string, category?: string): Promise<RecipesResponse> {
    const params = new URLSearchParams();
    if (searchTerm) params.append('search', searchTerm);
    if (category && category !== 'すべて') params.append('category', category);
    
    const queryString = params.toString();
    const endpoint = `/recipes${queryString ? `?${queryString}` : ''}`;
    
    return this.request<RecipesResponse>(endpoint);
  }

  async getRecipe(id: string): Promise<any> {
    return this.request<any>(`/recipes/${id}`);
  }

  async getCategories(): Promise<CategoriesResponse> {
    return this.request<CategoriesResponse>('/categories');
  }

  async createRecipe(recipeData: any): Promise<any> {
    return this.request<any>('/recipes', {
      method: 'POST',
      body: JSON.stringify(recipeData),
    });
  }

  async getRandomImage(): Promise<ImageResponse> {
    return this.request<ImageResponse>('/images/random');
  }

  async getAllImages(): Promise<ImagesResponse> {
    return this.request<ImagesResponse>('/images');
  }
}

export const apiService = new ApiService();