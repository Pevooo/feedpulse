import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import {
  Component,
  OnInit,
  OnDestroy,
} from '@angular/core';
import { FormsModule } from '@angular/forms';
import {
  DomSanitizer,
  SafeUrl,
} from '@angular/platform-browser';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';

import { TranslateModule } from '@ngx-translate/core';

import { ChatbotComponent } from './chatbot/chatbot.component';
import { PageAnalyticsService } from '../../app/services/page-analytics.service';

@Component({
  selector: 'app-page-analytics',
  standalone: true,
  imports: [CommonModule, FormsModule, ChatbotComponent,TranslateModule],
  templateUrl: './page-analytics.component.html',
  styleUrls: ['./page-analytics.component.css']
})
export class PageAnalyticsComponent implements OnInit, OnDestroy {
  facebookId = '';
  startDate = '';
  endDate = '';
  chartImages: SafeUrl[] = [];
  goals: string[] = [];
  pageName = '';
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  metrics: any;
  
  private subscription: Subscription = new Subscription();

  constructor(
    private router: Router,
    private http: HttpClient,
    private sanitizer: DomSanitizer,
    private pageAnalyticsService: PageAnalyticsService
  ) {}

  ngOnInit(): void {
    // Get data from service instead of query parameters
    const analyticsData = this.pageAnalyticsService.getAnalyticsData();
    
    if (analyticsData) {
      this.facebookId = analyticsData.facebookId;
      this.pageName = analyticsData.pageName;
    } else {
      // If no data in service, redirect back to dashboard
      console.warn('No analytics data found, redirecting to dashboard');
      this.router.navigate(['/dashboard']);
    }
  }

  ngOnDestroy(): void {
    // Clean up subscription
    this.subscription.unsubscribe();
    
    // Clear the analytics data from service when leaving the component
    this.pageAnalyticsService.clearAnalyticsData();
  }

  getAnalytics() {
    if (!this.startDate || !this.endDate) {
      alert('Please select both start and end dates.');
      return;
    }
    const formatToPythonIso = (date: string) => {
      return new Date(date).toISOString().replace('Z', '');
    };
    const apiUrl = `https://feedpulse.francecentral.cloudapp.azure.com/report`; // replace with your actual API
    const body = {
      page_id: this.facebookId,
      start_date: formatToPythonIso(this.startDate),
      end_date: formatToPythonIso(this.endDate)
    };

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    this.http.post<any>(apiUrl, body).subscribe({
      next: (res) => {
        if (res.status === 'SUCCESS') {
          this.goals = res.body.goals || [];
          this.chartImages = res.body.chart_rasters?.map((b64: string) =>
            this.sanitizer.bypassSecurityTrustUrl(`data:image/png;base64,${b64}`)
          ) || [];
          this.metrics = res.body.metrics || {};
        } else {
          console.error('❌ API returned failure:', res);
        }
      },
      error: (err) => {
        console.error('❌ Error fetching analytics:', err);
      }
    });
  }

  getMetricKeys(metricKey: string): string[] {
  if (this.metrics && this.metrics[metricKey]) {
    return Object.keys(this.metrics[metricKey]);
  }

  return [];
}
  formatValue(value: string): string {
    return value.split('_')
      .map(
        (v: string) => v[0].toUpperCase() + v.slice(1)
      ).join(' ');
  }
}
