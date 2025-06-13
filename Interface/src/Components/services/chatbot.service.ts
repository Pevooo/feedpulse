import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment.development';

export interface ChatMessage {
  id?: number;
  content: string;
  isUser: boolean;
  timestamp: Date;
  isRaster?: boolean;
}

export interface ChatRequest {
  page_id: string;
  start_date: string;
  end_date: string;
  question: string;
}

export interface ChatResponseBody {
  data: string;
  isRaster: number;
}

export interface ChatResponseData {
  status: string;
  body: ChatResponseBody;
}

export interface ApiResponse<T> {
  statusCode: number;
  meta: any;
  succeeded: boolean;
  message: string;
  
  errors: any;
  data: T;
}

@Injectable({
  providedIn: 'root'
})
export class ChatbotService {
  private apiUrl = `${environment.apiUrl}/api/v1/organization/chat`;

  constructor(private http: HttpClient) { }

  sendMessage(request: ChatRequest): Observable<ApiResponse<ChatResponseData>> {
    return this.http.post<ApiResponse<ChatResponseData>>(this.apiUrl, request);
  }
} 