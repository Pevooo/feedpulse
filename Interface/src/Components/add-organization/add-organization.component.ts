import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { Organization } from '../../app/interfaces/Organization';
import { OrganizationService } from '../../app/services/organization.service';
import Swal from 'sweetalert2';


@Component({
  selector: 'app-add-organization',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './add-organization.component.html',
  styleUrls: ['./add-organization.component.css']
})
export class AddOrganizationComponent implements OnInit {
  organization: Organization = {
    name: '',
    description: '',
    pageAccessToken: '',
    facebookId: '',
    userId: ''
  };

  constructor(private route: ActivatedRoute, private router: Router,

    private organizationService:OrganizationService
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.organization.name = params['name'] || '';
      this.organization.pageAccessToken = params['pageAccessToken'] || '';
      this.organization.facebookId = params['facebookId'] || '';
      this.organization.userId = params['userId'] || '';
    });
  }

  submitForm() {
    this.organizationService.addOrganization(this.organization).subscribe({
      next: () => {
        Swal.fire({
          icon: 'success',
          title: 'Success!',
          text: 'Organization added successfully.',
          confirmButtonText: 'OK'
        }).then(() => {
          this.router.navigate(['/dashboard']); // ✅ Redirect to dashboard
        });
      },
      error: (err) => {
        console.error('❌ Error adding organization:', err);
        Swal.fire({
          icon: 'error',
          title: 'Submission Failed!',
          text: 'An error occurred while adding the organization. Please try again.',
        });
      }
    });
  }
}
