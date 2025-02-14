import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Component } from '@angular/core';
import { RouterLink, RouterOutlet } from '@angular/router';
import {  NgForm,ReactiveFormsModule, FormsModule } from '@angular/forms';
import { IRegistrationModel } from '../../app/interfaces/IRegisterModel';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [RouterLink,RouterOutlet,CommonModule,HttpClientModule,ReactiveFormsModule,FormsModule],
  templateUrl: './signup.component.html',
  styleUrl: './signup.component.css'
})
export class SignupComponent  {
  registration:IRegistrationModel=
  {
    fullName: '',
    userName: '',
    email: '',
    password: '',
    confirmPassword: '',
    country: '',
    address: '',
    phoneNumber: '',
  };
  constructor(private http: HttpClient){
   
  }

  onSubmit(form:NgForm):void {
    if (form.valid) {
      console.log('Form Data:', this.registration);
      // You can now send this.registration to your backend or handle it as needed
    } else {
      console.log('Form is invalid');
    }
  }
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  onFileChange(event: any) {
    const file = event.target.files[0];
    if (file) {
      // Check if the file is an image
      if (this.isImageFile(file)) {
        this.convertToBase64(file).then((base64) => {
          this.registration.photo = base64; // Store Base64 string
           // Store the file object
        }).catch((error) => {
          console.error('Error converting file to Base64:', error);
        });
      } else {
        alert('Please upload a valid image file (JPEG, PNG, etc.).');
        this.registration.photo = "";
      }
    }
  }
  isImageFile(file: File): boolean {
    const acceptedImageTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
    return file && acceptedImageTypes.includes(file.type);
  }
  convertToBase64(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result as string);
      reader.onerror = (error) => reject(error);
    });
  }
}
