import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { AddOrganizationComponent } from './add-organization.component';
import { ActivatedRoute } from '@angular/router';
import { of } from 'rxjs';

describe('AddOrganizationComponent', () => {
  let component: AddOrganizationComponent;
  let fixture: ComponentFixture<AddOrganizationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule,
        AddOrganizationComponent, // ✅ Standalone component
      ],
      providers: [
        {
          provide: ActivatedRoute,
          useValue: {
            queryParams: of({
              name: 'Test Organization',
              pageAccessToken: 'abc123',
              facebookId: 'fb_001',
              userId: 'user_001'
            }),
            snapshot: { paramMap: { get: () => '123' } }
          }
        }
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(AddOrganizationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
