import { Component, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import {
  ActivatedRoute,
  Router,
  RouterLink
} from '@angular/router';

import {
  Categoria,
  CategoriasService
} from '../../services/categorias.service';

import {
  ProductoUpdate,
  ProductosService
} from '../../services/productos.service';

import {
  UploadsService
} from '../../services/uploads.service';


@Component({
  selector: 'app-admin-producto-editar',
  imports: [
    FormsModule,
    RouterLink
  ],
  templateUrl: './admin-producto-editar.html',
  styleUrl: './admin-producto-editar.css'
})
export class AdminProductoEditar implements OnInit {

  idProducto = 0;

  categorias = signal<Categoria[]>([]);

  idCategoria: number | null = null;
  codigo = '';
  nombre = '';
  descripcion = '';
  material = '';
  color = '';
  estilo = '';
  precio: number | null = null;

  imagenUrl: string | null = null;
  archivoImagen: File | null = null;

  cargando = signal(true);
  guardando = signal(false);
  error = signal('');


  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private productosService: ProductosService,
    private categoriasService: CategoriasService,
    private uploadsService: UploadsService
  ) {}


  ngOnInit(): void {

    this.idProducto = Number(
      this.route.snapshot.paramMap.get('id')
    );


    this.categoriasService
      .obtenerTodasAdmin()
      .subscribe({

        next: (categorias) => {
          this.categorias.set(categorias);
        }

      });


    this.productosService
      .obtenerProducto(this.idProducto)
      .subscribe({

        next: (producto) => {

          this.idCategoria =
            producto.id_categoria;

          this.codigo =
            producto.codigo;

          this.nombre =
            producto.nombre;

          this.descripcion =
            producto.descripcion || '';

          this.material =
            producto.material || '';

          this.color =
            producto.color || '';

          this.estilo =
            producto.estilo || '';

          this.precio =
            Number(producto.precio);

          this.imagenUrl =
            producto.imagen_url;

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


  seleccionarImagen(
    event: Event
  ): void {

    const input =
      event.target as HTMLInputElement;

    const archivo =
      input.files?.[0];


    if (!archivo) {
      this.archivoImagen = null;
      return;
    }


    const tiposPermitidos = [
      'image/jpeg',
      'image/png',
      'image/webp'
    ];


    if (
      !tiposPermitidos.includes(
        archivo.type
      )
    ) {

      this.error.set(
        'La imagen debe ser JPG, PNG o WEBP'
      );

      input.value = '';

      this.archivoImagen = null;

      return;
    }


    if (
      archivo.size >
      5 * 1024 * 1024
    ) {

      this.error.set(
        'La imagen no puede superar los 5 MB'
      );

      input.value = '';

      this.archivoImagen = null;

      return;
    }


    this.archivoImagen = archivo;

    this.error.set('');
  }


  guardarProducto(): void {

    if (
      !this.idCategoria ||
      !this.codigo.trim() ||
      !this.nombre.trim() ||
      this.precio === null
    ) {

      this.error.set(
        'Completa categoría, código, nombre y precio'
      );

      return;
    }


    if (this.precio < 0) {

      this.error.set(
        'El precio no puede ser negativo'
      );

      return;
    }


    this.guardando.set(true);
    this.error.set('');


    if (this.archivoImagen) {

      this.uploadsService
        .subirImagen(this.archivoImagen)
        .subscribe({

          next: (respuesta) => {

            this.actualizarProducto(
              respuesta.imagen_url
            );
          },

          error: (error) => {

            this.guardando.set(false);

            this.error.set(
              error.error?.detail ||
              'No se pudo subir la nueva imagen'
            );
          }

        });

    } else {

      this.actualizarProducto(
        this.imagenUrl
      );
    }
  }


  private actualizarProducto(
    imagenUrl: string | null
  ): void {

    const producto: ProductoUpdate = {

      id_categoria:
        this.idCategoria!,

      codigo:
        this.codigo.trim(),

      nombre:
        this.nombre.trim(),

      descripcion:
        this.descripcion.trim() || null,

      material:
        this.material.trim() || null,

      color:
        this.color.trim() || null,

      estilo:
        this.estilo.trim() || null,

      precio:
        this.precio!,

      imagen_url:
        imagenUrl
    };


    this.productosService
      .actualizarProducto(
        this.idProducto,
        producto
      )
      .subscribe({

        next: () => {

          this.router.navigate([
            '/admin/productos'
          ]);
        },

        error: (error) => {

          this.guardando.set(false);

          this.error.set(
            error.error?.detail ||
            'No se pudo actualizar el producto'
          );
        }

      });
  }

}