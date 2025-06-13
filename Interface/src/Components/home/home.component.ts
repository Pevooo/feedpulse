import { Component, HostListener, OnDestroy  } from '@angular/core';
import { RouterLink} from '@angular/router';
import { AuthService } from '../../app/services/auth.service';
import { CommonModule } from '@angular/common';  // Import CommonModule
import { ServicesComponent } from '../services/services.component';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterLink, ServicesComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent implements OnDestroy {
  isLoggedIn = this.authService.isLoggedIn();
  constructor(private authService: AuthService) {}

  // Make sure ngOnInit is correctly defined
  ngOnDestroy(): void {
    console.log("ngOnInit is called");
    this.isLoggedIn = this.authService.isLoggedIn();  // Set initial login state
  }

  onButtonClick() {
    console.log('GIF button clicked!');
    // Or navigate / do something else
  }

  @HostListener('window:scroll', [])
  onWindowScroll() {
    const timelineItems = document.querySelectorAll('.vertical-scrollable-timeline li');
    const timeline = document.querySelector('.vertical-scrollable-timeline');
    const progress = document.querySelector('.list-progress .inner') as HTMLElement;

    timelineItems.forEach((item) => {
      const rect = item.getBoundingClientRect();
      const windowHeight = window.innerHeight;

      if (rect.top >= 0 && rect.top <= windowHeight / 2) {
        item.classList.add('active');
      } else {
        item.classList.remove('active');
      }
    });

    // Update progress bar
    if (timeline && progress) {
      const windowHeight = window.innerHeight;
      const scrollTop = window.scrollY;
      const offsetTop = timeline.getBoundingClientRect().top + scrollTop;
      const totalHeight = timeline.scrollHeight - windowHeight;
      const scrolled = scrollTop - offsetTop;

      const progressPercent = Math.min(Math.max((scrolled / totalHeight) * 100, 0), 100);
      progress.style.height = `${progressPercent}%`;
    }
  }
}
