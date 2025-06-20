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

import { TranslateModule } from '@ngx-translate/core';

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
Model:SignInModel={ userName: "", password: "" };

constructor(private authService: AuthService,private router:Router) {

}
onSubmit(){
  //form;
this.authService.login(this.Model.userName,this.Model.password).subscribe({
  next:(response)=>{
    if(response.succeeded&&response.data){
      localStorage.setItem('accessToken', response.data.accessToken);
      localStorage.setItem('refreshToken', response.data.refreshToken.token);



       // const decoded = jwtDecode(response.data.accessToken) as JwtPayload;
        //console.log('decoded',decoded);


      console.log('Access Token:', response.data.accessToken);
      console.log('Refresh Token:', response.data.refreshToken);
      Swal.fire({
        icon: 'success',
        title: 'Login Successful',
        text: 'Welcome back!',
        timer: 1500,
        showConfirmButton: false
      }).then(() => {
        this.router.navigate(['/']);
      });
    }else{
      console.log("LoginFaild1"+response.message);
    }
  },
  error:(err)=>{
    console.log(err);
    Swal.fire({
      icon: 'error',
      title: 'Login Failed',
      text: err.error.message || 'Invalid credentials.',
      confirmButtonColor: '#20c0bd', // Change this to your desired color
      confirmButtonText: 'OK' // Explicitly set the button text if needed
    });
  }
})

}

}
