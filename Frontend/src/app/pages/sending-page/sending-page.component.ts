import { Component } from '@angular/core';

@Component({
  selector: 'app-sending-page',
  templateUrl: './sending-page.component.html',
  styleUrls: ['./sending-page.component.scss']
})
export class SendingPageComponent {
  toggle = true;
  status = '../../../assets/icons/play.svg';
  state = "Время рассылки";

  enableDisableRule() {
    this.toggle = !this.toggle;
    this.status = this.toggle ? '../../../assets/icons/play.svg' : '../../../assets/icons/pause.svg';
    this.state = this.toggle ? "Время рассылки" : "Идет рассылка";
  }
}
