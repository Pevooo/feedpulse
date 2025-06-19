import { isPlatformBrowser } from '@angular/common';
import {
  Inject,
  Injectable,
  PLATFORM_ID,
} from '@angular/core';

import { TranslateService } from '@ngx-translate/core';

@Injectable({ providedIn: 'root' })
export class LanguageService {
  private isBrowser: boolean;

  constructor(
    private translate: TranslateService,
    @Inject(PLATFORM_ID) private platformId: object
  ) {
    this.isBrowser = isPlatformBrowser(platformId);

    translate.addLangs(['en', 'ar']);
    translate.setDefaultLang('en');

    const savedLang = this.isBrowser ? localStorage.getItem('lang') : 'en';
    this.setDirection(savedLang || 'en');
    translate.use(savedLang || 'en');
  }

  switchLang(lang: string) {
    this.translate.use(lang);
    this.setDirection(lang);
    if (this.isBrowser) {
      localStorage.setItem('lang', lang);
    }
  }

  getCurrentLang(): string {
    return this.translate.currentLang;
  }

  private setDirection(lang: string) {
    if (this.isBrowser) {
      const dir = lang === 'ar' ? 'rtl' : 'ltr';
      document.documentElement.setAttribute('dir', dir);
      document.documentElement.setAttribute('lang', lang);
    }
  }
}
