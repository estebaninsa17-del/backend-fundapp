import { NextResponse } from 'next/server';
import { createClient } from '@/lib/supabase/server';

export async function GET() {
  try {
    const supabase = await createClient();

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

    return NextResponse.json({ totalVoluntarios: totalVoluntarios || 0, actividadesActivas: actividadesActivas || 0, montoTotal });
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
