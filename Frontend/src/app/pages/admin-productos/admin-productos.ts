import {
  Component,
  OnInit,
  signal
} from '@angular/core';

import {
  RouterLink
} from '@angular/router';

import {
  Producto,
  ProductosService
} from '../../services/productos.service';


@Component({
  selector: 'app-admin-productos',

  imports: [
    RouterLink
  ],

  templateUrl: './admin-productos.html',

  styleUrl: './admin-productos.css'
})
export class AdminProductos implements OnInit {

  productos = signal<Producto[]>([]);

  cargando = signal(true);

  error = signal('');


  constructor(
    private productosService: ProductosService
  ) {}


  ngOnInit(): void {

    this.cargarProductos();

  }


  cargarProductos(): void {

    this.cargando.set(true);

    this.error.set('');


    this.productosService
      .obtenerTodosAdmin()
      .subscribe({

        next: (datos) => {

          this.productos.set(datos);

          this.cargando.set(false);

        },


        error: () => {

          this.error.set(
            'No se pudieron cargar los productos'
          );

          this.cargando.set(false);

        }

      });

  }


  desactivarProducto(
    idProducto: number
  ): void {

    const confirmar = window.confirm(
      '¿Deseas desactivar este producto?'
    );


    if (!confirmar) {
      return;
    }


    this.productosService
      .desactivarProducto(idProducto)
      .subscribe({

        next: () => {

          this.cargarProductos();

        },


        error: () => {

          this.error.set(
            'No se pudo desactivar el producto'
          );

        }

      });

  }


  activarProducto(
    idProducto: number
  ): void {

    const confirmar = window.confirm(
      '¿Deseas activar nuevamente este producto?'
    );


    if (!confirmar) {
      return;
    }


    this.productosService
      .activarProducto(idProducto)
      .subscribe({

        next: () => {

          this.cargarProductos();

        },


        error: () => {

          this.error.set(
            'No se pudo activar el producto'
          );

        }

      });

  }

}