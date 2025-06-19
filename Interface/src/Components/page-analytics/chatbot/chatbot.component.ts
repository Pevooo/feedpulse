import { Component, OnInit, Input } from '@angular/core';
import { ChatbotService, ChatMessage, ChatRequest } from '../../services/chatbot.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DomSanitizer } from '@angular/platform-browser';
import { ElementRef, ViewChild } from '@angular/core';
import {animate, style, transition, trigger} from "@angular/animations";

@Component({
  selector: 'app-chatbot',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.css'],
  animations: [
    trigger('fadeInOut', [
      transition(':enter', [
        style({ opacity: 0, transform: 'translateY(10px)' }),
        animate('300ms ease-out', style({ opacity: 1, transform: 'translateY(0)' }))
      ]),
      transition(':leave', [
        animate('200ms ease-in', style({ opacity: 0 }))
      ])
    ])]
})
export class ChatbotComponent implements OnInit {
  @Input() facebookId = '';
  @Input() startDate = '';
  @Input() endDate = '';
  @Input() showChatbot = false;
  @ViewChild('chatMessages') chatMessages!: ElementRef;

  messages: ChatMessage[] = [];
  newMessage = '';
  isLoading = false;
  isOpen = false;

  constructor(
    private chatbotService: ChatbotService,
    private sanitizer: DomSanitizer
  ) {}

  ngOnInit() {
    this.messages = [];
  }

  sendMessage() {
    if (!this.newMessage.trim() || !this.facebookId || !this.startDate || !this.endDate) return;

    const userMessage: ChatMessage = {
      content: this.newMessage,
      isUser: true,
      timestamp: new Date(),
      icon: 'fa-user'
    };

    this.messages.push(userMessage);
    this.scrollToBottom();
    this.isLoading = true;
    this.newMessage = '';

    const request: ChatRequest = {
      page_id: this.facebookId,
      start_date: this.startDate,
      end_date: this.endDate,
      question: this.get_last_5_messages()
    };

    this.chatbotService.sendMessage(request).subscribe({
      next: (response) => {
        if (response.succeeded && response.data.status === 'SUCCESS') {
          const botMessage: ChatMessage = {
            content: response.data.body.isRaster === 1
              ? this.sanitizer.bypassSecurityTrustUrl(`data:image/png;base64,${response.data.body.data}`) as string
              : response.data.body.data,
            isUser: false,
            timestamp: new Date(),
            isRaster: response.data.body.isRaster === 1,
            icon: 'fas fa-robot'
          };
          this.messages.push(botMessage);
          this.scrollToBottom();
        }
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Error sending message:', error);
        const errorMessage: ChatMessage = {
          content: "An unexpected error occured. Please try again!",
          isUser: false,
          timestamp: new Date(),
          isRaster: false,
          icon: 'fa-triangle-exclamation'        
        }
        this.messages.push(errorMessage);
        this.scrollToBottom();
        this.isLoading = false;
      }
    });
  }
  scrollToBottom(): void {
    try {
      setTimeout(() => {
        this.chatMessages.nativeElement.scrollTo({
          top: this.chatMessages.nativeElement.scrollHeight,
          behavior: 'smooth' // 👈 this makes it smooth
        });
      }, 0); // allow DOM update
    } catch (err) {
      console.error('Could not scroll:', err);
    }
  }
  toggleChat() {
    if (this.showChatbot) {
      this.isOpen = !this.isOpen;
      if (this.isOpen) {
        this.scrollToBottom()
      }
    }
  }
  get_last_5_messages(): string {
    const strings: string[] = [];
    this.messages.slice(-3).forEach((message) => {
      if (message.isUser) {
        strings.push("USER: " + message.content);
      } else {
        if (message.isRaster) {
          strings.push("ASSISTANT: [chart]");
        } else {
          strings.push("ASSISTANT: " + message.content);
        }
      }
    });
    return strings.join("\n");
  }
}
