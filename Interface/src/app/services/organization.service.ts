import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment.development';
import { Observable } from 'rxjs';
import { Organization } from '../interfaces/Organization';

@Injectable({
  providedIn: 'root'
})
export class OrganizationService {
  private Url = environment.apiUrl + 'organization/create'; // 🔹 Adjust the endpoint as needed

  constructor(private http: HttpClient) {}

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  addOrganization(org: Organization): Observable<any> {
    const formData = new FormData();
    formData.append('Name', org.name);
    formData.append('Description', org.description);
    formData.append('FacebookId', org.facebookId);
    formData.append('PageAccessToken', org.pageAccessToken);
    formData.append('UserId', org.userId);

    return this.http.post(this.Url, formData);
  }
}