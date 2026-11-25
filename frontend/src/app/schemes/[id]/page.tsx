// Server Component — awaits params then delegates to client
export const instant = false; // dynamic route: opt out of instant static generation
import SchemeDetailContent from "./_scheme-detail";

export default async function SchemeDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return <SchemeDetailContent id={id} />;
}
