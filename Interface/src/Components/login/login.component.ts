import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { Component } from '@angular/core';
import {
  FormsModule,
  ReactiveFormsModule,
} from '@angular/forms';
import {
  Router,
  /*RouterLink,
  RouterOutlet,*/
} from '@angular/router';

import Swal from 'sweetalert2';

import {TranslateModule, TranslateService} from '@ngx-translate/core';

import { SignInModel } from '../../app/interfaces/ISignInModel';
import { AuthService } from '../../app/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports:[CommonModule,HttpClientModule,ReactiveFormsModule,FormsModule,TranslateModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent  {
Model: SignInModel={ userName: "", password: "" };

constructor(private authService: AuthService,private router:Router, private translate: TranslateService) {

}
onSubmit() {
  this.authService.login(this.Model.userName, this.Model.password).subscribe({
    next: (response) => {
      if (response.succeeded && response.data) {
        localStorage.setItem('accessToken', response.data.accessToken);
        localStorage.setItem('refreshToken', response.data.refreshToken.token);

        this.translate.get(['LOGIN_SUCCESS', 'WELCOME_BACK']).subscribe(translations => {
          Swal.fire({
            icon: 'success',
            title: translations['LOGIN_SUCCESSFUL'],
            text: translations['WELCOME_BACK'],
            timer: 1500,
            showConfirmButton: false
          }).then(() => {
            this.router.navigate(['/']);
          });
        });
      } else {
        console.log('LoginFailed: ' + response.message);
      }
    },
    error: (err) => {
      this.translate.get(['LOGIN_FAILED', 'INVALID_CREDENTIALS', 'OK']).subscribe(translations => {
        Swal.fire({
          icon: 'error',
          title: translations['LOGIN_FAILED'],
          text: err.error.message || translations['INVALID_CREDENTIALS'],
          confirmButtonColor: '#20c0bd',
          confirmButtonText: translations['OK']
        });
      });
    }
  });
}

}
