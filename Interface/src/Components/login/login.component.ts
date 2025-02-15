import {  HttpClientModule } from '@angular/common/http';
import { Component } from '@angular/core';
import { RouterLink, RouterOutlet } from '@angular/router';
import {  ReactiveFormsModule, FormsModule, Form } from '@angular/forms';

import { CommonModule } from '@angular/common';
import { SignInModel } from '../../app/interfaces/ISignInModel';

@Component({
  selector: 'app-login',
  standalone: true,
  imports:[RouterLink,RouterOutlet,CommonModule,HttpClientModule,ReactiveFormsModule,FormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent  {
Model:SignInModel={userName: " ",password:""};
/**
 *
 */
constructor() {
  //
  
}
onSubmit(form:Form){
console.log(form);

}

}
