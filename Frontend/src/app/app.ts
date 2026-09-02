import {
  Component,
  signal
} from '@angular/core';

import {
  NavigationEnd,
  Router,
  RouterOutlet
} from '@angular/router';

import {
  filter
} from 'rxjs';

import {
  Navbar
} from './components/navbar/navbar';

import {
  Footer
} from './components/footer/footer';


@Component({
  selector: 'app-root',
  imports: [
    RouterOutlet,
    Navbar,
    Footer
  ],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {

  esRutaAdmin = signal(false);


  constructor(
    private router: Router
  ) {

    this.actualizarRuta(
      this.router.url
    );


    this.router.events
      .pipe(
        filter(
          evento =>
            evento instanceof NavigationEnd
        )
      )
      .subscribe(
        evento => {

          this.actualizarRuta(
            evento.urlAfterRedirects
          );

        }
      );
  }


  private actualizarRuta(
    url: string
  ): void {

    this.esRutaAdmin.set(
      url.startsWith('/admin')
    );
  }

}