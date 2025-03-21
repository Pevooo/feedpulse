import { RefreshToken } from "./RefreshToken";

export interface AuthResponse {
  accessToken: string;
  refreshToken: RefreshToken;
}

