import { Component, OnInit, signal } from '@angular/core';
import {
  ActivatedRoute,
  RouterLink
} from '@angular/router';

import { CarritoService } from '../../services/carrito.service';

import {
  Producto,
  ProductosService
} from '../../services/productos.service';

import {
  RecomendacionResultado,
  RecomendacionesService
} from '../../services/recomendaciones.service';


@Component({
  selector: 'app-producto-detalle',
  imports: [
    RouterLink
  ],
  templateUrl: './producto-detalle.html',
  styleUrl: './producto-detalle.css'
})
export class ProductoDetalle implements OnInit {

  producto = signal<Producto | null>(null);

  recomendaciones =
    signal<RecomendacionResultado[]>([]);

  stockDisponible = signal<number | null>(null);

  mensajeCarrito = signal('');

  cargando = signal(true);
  error = signal('');


  constructor(
    private route: ActivatedRoute,
    private productosService: ProductosService,
    private carritoService: CarritoService,
    private recomendacionesService: RecomendacionesService
  ) {}


  ngOnInit(): void {

    this.route.paramMap.subscribe(params => {

      const id = Number(
        params.get('id')
      );


      if (!id) {

        this.error.set(
          'Producto no válido'
        );

        this.cargando.set(false);

        return;
      }


      this.mensajeCarrito.set('');
      this.stockDisponible.set(null);

      this.cargarProducto(id);

      this.cargarRecomendaciones(id);

      this.cargarDisponibilidad(id);

    });
  }


  cargarProducto(
    id: number
  ): void {

    this.cargando.set(true);
    this.error.set('');


    this.productosService
      .obtenerProducto(id)
      .subscribe({

        next: (producto) => {

          this.producto.set(
            producto
          );

          this.cargando.set(false);
        },

        error: () => {

          this.error.set(
            'No se pudo cargar el producto'
          );

          this.cargando.set(false);
        }

      });
  }


  cargarRecomendaciones(
    idProducto: number
  ): void {

    this.recomendaciones.set([]);


    this.recomendacionesService
      .obtenerRecomendaciones(
        idProducto
      )
      .subscribe({

        next: (resultados) => {

          this.recomendaciones.set(
            resultados
          );
        },

        error: () => {

          this.recomendaciones.set(
            []
          );
        }

      });
  }


  cargarDisponibilidad(
    idProducto: number
  ): void {

    this.productosService
      .obtenerDisponibilidad(
        idProducto
      )
      .subscribe({

        next: (respuesta) => {

          this.stockDisponible.set(
            respuesta.stock_disponible
          );
        },

        error: () => {

          this.stockDisponible.set(
            0
          );
        }

      });
  }


  agregarAlCarrito(
    producto: Producto
  ): void {

    const stock =
      this.stockDisponible();


    if (stock === null) {

      this.mensajeCarrito.set(
        'Consultando disponibilidad...'
      );

      return;
    }


    if (stock === 0) {

      this.mensajeCarrito.set(
        'Producto agotado'
      );

      return;
    }


    const itemActual =
      this.carritoService
        .items()
        .find(
          item =>
            item.producto.id_producto ===
            producto.id_producto
        );


    const cantidadActual =
      itemActual?.cantidad || 0;


    if (
      cantidadActual >= stock
    ) {

      this.mensajeCarrito.set(
        'No hay más unidades disponibles'
      );

      return;
    }


    this.carritoService
      .agregarProducto(
        producto
      );


    this.mensajeCarrito.set(
      'Producto agregado al carrito'
    );
  }

}