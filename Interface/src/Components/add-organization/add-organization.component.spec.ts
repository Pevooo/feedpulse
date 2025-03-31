import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddOrganizationComponent } from './add-organization.component';

describe('AddOrganizationComponent', () => {
  let component: AddOrganizationComponent;
  let fixture: ComponentFixture<AddOrganizationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AddOrganizationComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AddOrganizationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
