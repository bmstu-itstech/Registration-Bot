import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LoginCheckComponent } from './login-check.component';

describe('LoginCheckComponent', () => {
  let component: LoginCheckComponent;
  let fixture: ComponentFixture<LoginCheckComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [LoginCheckComponent]
    });
    fixture = TestBed.createComponent(LoginCheckComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
