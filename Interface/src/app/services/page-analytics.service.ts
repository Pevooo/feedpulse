import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

export interface PageAnalyticsData {
  facebookId: string;
  pageName: string;
  userId?: string;
  accessToken?: string;
}

@Injectable({
  providedIn: 'root'
})
export class PageAnalyticsService {
  private analyticsDataSubject = new BehaviorSubject<PageAnalyticsData | null>(null);
  public analyticsData$ = this.analyticsDataSubject.asObservable();

  setAnalyticsData(data: PageAnalyticsData): void {
    this.analyticsDataSubject.next(data);
  }

  getAnalyticsData(): PageAnalyticsData | null {
    return this.analyticsDataSubject.value;
  }

  clearAnalyticsData(): void {
    this.analyticsDataSubject.next(null);
  }
} 