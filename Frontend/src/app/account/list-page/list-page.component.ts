import {Component, ViewChild} from '@angular/core';
import {CarouselComponent} from "ngx-bootstrap/carousel";

@Component({
  selector: 'app-list-page',
  templateUrl: './list-page.component.html',
  styleUrls: ['./list-page.component.scss']
})
export class ListPageComponent {
  @ViewChild('carousel') carousel: CarouselComponent | undefined;
  cards = [
    {
      title: 'Бот 1',
      creationDate: '00.00.0000',
      numMembers: 'N человек',
    },
    {
      title: 'Бот 2',
      creationDate: '00.00.0000',
      numMembers: 'N человек',
    },
    {
      title: 'Бот 3',
      creationDate: '00.00.0000',
      numMembers: 'N человек',
    },
    {
      title: 'Бот 4',
      creationDate: '00.00.0000',
      numMembers: 'N человек',
    }
  ]
  navigateCarousel(direction: string) {
    const carousel = document.querySelector('.carousel') as HTMLElement | null;
    if (carousel) {
      if (direction === 'prev') {
        const prevButton = carousel.querySelector('.carousel-control-prev') as HTMLElement | null;
        prevButton?.click();
      } else if (direction === 'next') {
        const nextButton = carousel.querySelector('.carousel-control-next') as HTMLElement | null;
        nextButton?.click();
      }
    }
  }
}
