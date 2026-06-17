import { NextResponse } from 'next/server';
import { createClient } from '@/lib/supabase/server';
import { verifyToken } from '@/services/auth.service';

export async function GET(req: Request) {
  try {
    const authHeader = req.headers.get('Authorization');
    const token = authHeader?.split(' ')[1];
    const user = token ? verifyToken(token) : null;
    const isAdmin = user && user.rol === 'admin';

    const supabase = await createClient();

    if (isAdmin) {
      const [
        { count: usuariosActivos },
        { count: totalVoluntarios },
        { count: actividadesActivas },
        { count: donacionesConfirmadas },
        { data: postulacionesData, count: postulacionesPendientes },
        { data: montoData },
        { data: ultimasDonaciones },
        { data: ultimasPostulaciones }
      ] = await Promise.all([
        supabase.schema('usuarios').from('usuarios').select('*', { count: 'exact', head: true }).eq('estadodecuenta', 'Activo'),
        supabase.schema('voluntariado').from('voluntarios').select('*', { count: 'exact', head: true }),
        supabase.schema('voluntariado').from('actividades').select('*', { count: 'exact', head: true }).gte('fechafin', new Date().toISOString().split('T')[0]),
        supabase.schema('donaciones').from('donaciones').select('*', { count: 'exact', head: true }).eq('estadopago', 'Confirmada'),
        supabase.schema('voluntariado').from('postulaciones').select('*', { count: 'exact', head: true }).eq('estadopostulacion', 'Pendiente'),
        // Query to calculate sum
        supabase.schema('donaciones').from('donaciones').select('monto').eq('estadopago', 'Confirmada'),
        // Recent transactions
        supabase.schema('donaciones').from('donaciones').select('*').eq('estadopago', 'Confirmada').order('fechadonacion', { ascending: false }).limit(5),
        supabase.schema('voluntariado').from('postulaciones').select('*, voluntarios(*), actividades(*)').order('fechapostulacion', { ascending: false }).limit(5)
      ]);

      const montoTotal = montoData?.reduce((sum, d) => sum + (d.monto || 0), 0) || 0;

      // Cross-schema manual join for usuarios
      const userIds = new Set<number>();
      ultimasDonaciones?.forEach((d: any) => { if (d.usuarios_idusuarios) userIds.add(d.usuarios_idusuarios); });
      ultimasPostulaciones?.forEach((p: any) => { if (p.voluntarios?.usuarios_idusuarios) userIds.add(p.voluntarios.usuarios_idusuarios); });

      let usuariosMap: any = {};
      if (userIds.size > 0) {
        const { data: usersData } = await supabase.schema('usuarios').from('usuarios').select('*').in('idusuarios', Array.from(userIds));
        if (usersData) {
          usersData.forEach(u => usuariosMap[u.idusuarios] = u);
        }
      }

      const mappedDonaciones = ultimasDonaciones?.map((d: any) => ({ ...d, usuarios: usuariosMap[d.usuarios_idusuarios] })) || [];
      const mappedPostulaciones = ultimasPostulaciones?.map((p: any) => {
        let v = p.voluntarios || {};
        return {
          ...p,
          voluntarios: {
            ...v,
            usuarios: usuariosMap[v.usuarios_idusuarios]
          }
        }
      }) || [];

      return NextResponse.json({
        usuariosActivos: usuariosActivos || 0,
        totalVoluntarios: totalVoluntarios || 0,
        actividadesActivas: actividadesActivas || 0,
        donacionesConfirmadas: donacionesConfirmadas || 0,
        montoTotal,
        postulacionesPendientes: postulacionesPendientes || 0,
        ultimasDonaciones: mappedDonaciones,
        ultimasPostulaciones: mappedPostulaciones
      });
    } else {
      // Public aggregates view
      const [
        { count: totalVoluntarios },
        { count: actividadesActivas },
        { data: montoData }
      ] = await Promise.all([
        supabase.schema('voluntariado').from('voluntarios').select('*', { count: 'exact', head: true }),
        supabase.schema('voluntariado').from('actividades').select('*', { count: 'exact', head: true }),
        supabase.schema('donaciones').from('donaciones').select('monto').eq('estadopago', 'Confirmada')
      ]);

      const montoTotal = montoData?.reduce((sum, d) => sum + (d.monto || 0), 0) || 0;

      return NextResponse.json({
        totalVoluntarios: totalVoluntarios || 0,
        actividadesActivas: actividadesActivas || 0,
        montoTotal
      });
    }
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
