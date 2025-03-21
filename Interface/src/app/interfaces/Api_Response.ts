export interface ApiResponse<T> {
    statusCode: number;
    meta: unknown | null;
    succeeded: boolean;
    message: string;
    errors: unknown | null;
    data: T | null;
  }