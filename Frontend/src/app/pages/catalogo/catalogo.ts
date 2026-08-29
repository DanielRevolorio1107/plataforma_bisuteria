import { Component, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';

import {
  Producto,
  ProductosService
} from '../../services/productos.service';


@Component({
  selector: 'app-catalogo',
  imports: [
    RouterLink,
    FormsModule
  ],
  templateUrl: './catalogo.html',
  styleUrl: './catalogo.css'
})
export class Catalogo implements OnInit {

  productos = signal<Producto[]>([]);

  consulta = '';

  cargando = signal(true);
  buscando = signal(false);
  error = signal('');
  busquedaActiva = signal(false);


  constructor(
    private productosService: ProductosService
  ) {}


  ngOnInit(): void {
    this.cargarProductos();
  }


  cargarProductos(): void {

    this.cargando.set(true);
    this.error.set('');
    this.busquedaActiva.set(false);

    this.productosService.obtenerProductos().subscribe({

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


  buscar(): void {

    const texto = this.consulta.trim();

    if (!texto) {
      this.cargarProductos();
      return;
    }

    this.buscando.set(true);
    this.error.set('');

    this.productosService
      .buscarProductos(texto)
      .subscribe({

        next: (resultados) => {

          this.productos.set(
            resultados.map(
              resultado => resultado.producto
            )
          );

          this.busquedaActiva.set(true);
          this.buscando.set(false);
        },

        error: () => {

          this.error.set(
            'No se pudo realizar la búsqueda'
          );

          this.buscando.set(false);
        }

      });
  }


  limpiarBusqueda(): void {

    this.consulta = '';
    this.cargarProductos();
  }

}