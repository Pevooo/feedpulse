import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import {
  Component,
  OnInit,
} from '@angular/core';
import { FormsModule } from '@angular/forms';
import {
  DomSanitizer,
  SafeUrl,
} from '@angular/platform-browser';
import { ActivatedRoute } from '@angular/router';
import { ChatbotComponent } from './chatbot/chatbot.component';

@Component({
  selector: 'app-page-analytics',
  standalone: true,
  imports: [CommonModule, FormsModule, ChatbotComponent],
  templateUrl: './page-analytics.component.html',
  styleUrls: ['./page-analytics.component.css']
})
export class PageAnalyticsComponent implements OnInit {
  facebookId = '';
  startDate = '';
  endDate = '';
  chartImages: SafeUrl[] = [];
  goals: string[] = [];
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  metrics: any;
  constructor(private route: ActivatedRoute,
     private http: HttpClient,
     private sanitizer: DomSanitizer
    ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.facebookId = params['facebookId'];
    });
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
