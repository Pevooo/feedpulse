import { Component, OnInit, Input } from '@angular/core';
import { ChatbotService, ChatMessage, ChatRequest } from '../../services/chatbot.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-chatbot',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.css']
})
export class ChatbotComponent implements OnInit {
  @Input() facebookId = '';
  @Input() startDate = '';
  @Input() endDate = '';
  @Input() showChatbot = false;

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
      timestamp: new Date()
    };

    this.messages.push(userMessage);
    this.isLoading = true;
    this.newMessage = '';

    const request: ChatRequest = {
      page_id: this.facebookId,
      start_date: this.startDate,
      end_date: this.endDate,
      question: userMessage.content
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
            isRaster: response.data.body.isRaster === 1
          };
          this.messages.push(botMessage);
        }
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Error sending message:', error);
        this.isLoading = false;
      }
    });
  }

  toggleChat() {
    if (this.showChatbot) {
      this.isOpen = !this.isOpen;
    }
  }
}
