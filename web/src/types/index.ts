export interface User {
  id: number;
  username: string;
  email: string;
  created_at?: string;
}

export interface Photo {
  id: number;
  item_id: number;
  file_path: string;
  is_primary: boolean;
  created_at?: string;
}

export interface Item {
  id: number;
  user_id: number;
  manufacturer: string;
  author_form: string;
  author_decoration: string;
  form_name: string;
  decoration_name: string;
  year: string;
  period: string;
  material: string;
  condition: string;
  size: string;
  location: string;
  comment: string;
  is_public: boolean;
  photos?: Photo[];
  created_at?: string;
  updated_at?: string;
  owner_username?: string;
}

export interface LoginData {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}
