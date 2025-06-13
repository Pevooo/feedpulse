import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment.development';
import { Observable } from 'rxjs';
import { Organization } from '../interfaces/Organization';

@Injectable({
  providedIn: 'root'
})
export class OrganizationService {
  private Url = environment.apiUrl + '/api/v1/organization/create'; // 🔹 Adjust the endpoint as needed

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
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  getUnRegisterdOrganization(token:string):Observable<any>{
    //const params = new HttpParams().set('AccessToken', token);
    return this.http.get(`https://feedpulse-d0ebhmb4gucybhdg.italynorth-01.azurewebsites.net/api/facebook/unregisteredpages`, {
      params: {
        AccessToken: token
      }
    });
  }
}
/**
 *
 */
