import { ComponentFixture, TestBed } from '@angular/core/testing';
import { LoginComponent } from './login.component';
import { ActivatedRoute } from '@angular/router';
import { ReactiveFormsModule } from '@angular/forms';  // For reactive forms
import { HttpClientModule } from '@angular/common/http';  // Import HttpClientModule to provide HttpClient
import { AuthService } from '../../app/services/auth.service';  // Import AuthService for dependency injection
import { TranslateModule } from '@ngx-translate/core';

describe('LoginComponent', () => {
  let component: LoginComponent;
  let fixture: ComponentFixture<LoginComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LoginComponent, ReactiveFormsModule, HttpClientModule,TranslateModule.forRoot()],  // Add HttpClientModule here
      providers: [
        { provide: ActivatedRoute, useValue: { snapshot: { paramMap: {} } } },  // Mock ActivatedRoute
        AuthService  // Provide AuthService
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LoginComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
