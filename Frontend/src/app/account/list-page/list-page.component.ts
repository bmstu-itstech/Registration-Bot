import {Component, ViewChild, AfterViewInit, Renderer2} from '@angular/core';
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

  constructor(private renderer: Renderer2) {}
  currentSlideIndex = 0;
  ngAfterViewInit() {
    this.checkDeadEnd();
  }
  navigateCarousel(direction: string) {
    const carousel = document.querySelector('.carousel') as HTMLElement | null;
    if (carousel) {
      if (direction === 'prev') {
        const prevButton = carousel.querySelector('.carousel-control-prev') as HTMLElement | null;
        prevButton?.click();
        this.currentSlideIndex--;
        this.checkDeadEnd();
      } else if (direction === 'next') {
        const nextButton = carousel.querySelector('.carousel-control-next') as HTMLElement | null;
        nextButton?.click();
        this.currentSlideIndex++;
        this.checkDeadEnd();
      }
    }
  }
  checkDeadEnd() {
    let totalSlides;
    if (this.cards.length <= 3) {
      totalSlides = 1;
    } else {
      totalSlides = this.cards.length-2;
    }
    const leftCursor = document.querySelector('.prev') as HTMLElement | null;
    const rightCursor = document.querySelector('.next') as HTMLElement | null;
    const slide = document.querySelector('.slide') as HTMLElement | null;
    if (this.currentSlideIndex === 0 && leftCursor && slide) {
      leftCursor.style.display = 'none';
      this.renderer.setStyle(slide, 'margin-left', '238px');
    } else if (leftCursor) {
      leftCursor.style.display = 'block';
      this.renderer.removeStyle(slide, 'margin-left');
    }
    if (this.currentSlideIndex === totalSlides - 1 && rightCursor && slide) {
      rightCursor.style.display = 'none';
      this.renderer.setStyle(slide, 'margin-right', '238px');
    } else if (rightCursor) {
      rightCursor.style.display = 'block';
      this.renderer.removeStyle(slide, 'margin-right');
    }
  }
}
