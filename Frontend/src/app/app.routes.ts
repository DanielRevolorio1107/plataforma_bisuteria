import { Routes } from '@angular/router';
import { Catalogo } from './pages/catalogo/catalogo';
import { ProductoDetalle } from './pages/producto-detalle/producto-detalle';
import { Carrito } from './pages/carrito/carrito';
import { Checkout } from './pages/checkout/checkout';
import { PedidoConfirmado } from './pages/pedido-confirmado/pedido-confirmado';
import { AdminLogin } from './pages/admin-login/admin-login';
import { AdminDashboard } from './pages/admin-dashboard/admin-dashboard';
import { authGuard } from './guards/auth-guard';
import { AdminProductos } from './pages/admin-productos/admin-productos';
import { AdminProductoNuevo } from './pages/admin-producto-nuevo/admin-producto-nuevo';
import { AdminCategorias } from './pages/admin-categorias/admin-categorias';
import { AdminInventario } from './pages/admin-inventario/admin-inventario';
import { AdminPedidos } from './pages/admin-pedidos/admin-pedidos';
import { AdminPedidoDetalle } from './pages/admin-pedido-detalle/admin-pedido-detalle';
import { AdminCategoriaNueva } from './pages/admin-categoria-nueva/admin-categoria-nueva';
import { AdminCategoriaEditar } from './pages/admin-categoria-editar/admin-categoria-editar';
import { AdminProductoEditar } from './pages/admin-producto-editar/admin-producto-editar';

export const routes: Routes = [
  {
    path: '',
    component: Catalogo
  },
  {
    path: 'productos/:id',
    component: ProductoDetalle
  }, 
   {
    path: 'carrito',
    component: Carrito
  },
  {
  path: 'checkout',
  component: Checkout
},
{
  path: 'pedido-confirmado/:id',
  component: PedidoConfirmado
},
{
  path: 'admin/login',
  component: AdminLogin
},
{
  path: 'admin',
  component: AdminDashboard,
  canActivate: [authGuard]
}, 
{
  path: 'admin/productos',
  component: AdminProductos,
  canActivate: [authGuard]
},
{
  path: 'admin/productos/nuevo',
  component: AdminProductoNuevo,
  canActivate: [authGuard]
},
{
  path: 'admin/categorias',
  component: AdminCategorias,
  canActivate: [authGuard]
},
{
  path: 'admin/inventario',
  component: AdminInventario,
  canActivate: [authGuard]
},
{
  path: 'admin/pedidos',
  component: AdminPedidos,
  canActivate: [authGuard]
},
{
  path: 'admin/pedidos/:id',
  component: AdminPedidoDetalle,
  canActivate: [authGuard]
},
{
  path: 'admin/categorias/nueva',
  component: AdminCategoriaNueva,
  canActivate: [authGuard]
},
{
  path: 'admin/categorias/editar/:id',
  component: AdminCategoriaEditar,
  canActivate: [authGuard]
},
{
  path: 'admin/productos/editar/:id',
  component: AdminProductoEditar,
  canActivate: [authGuard]
}
];