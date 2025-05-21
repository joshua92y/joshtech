//src/app/blog/[slug]/page.tsx
import { notFound } from "next/navigation";
import { CustomMDX } from "@/components/mdx";
import { getPosts } from "@/app/utils/utils";
import {
  AvatarGroup,
  Button,
  Column,
  Heading,
  HeadingNav,
  Icon,
  Row,
  Text,
} from "@/once-ui/components";
import { about, blog, person, baseURL } from "@/app/resources";
import { formatDate } from "@/app/utils/formatDate";
import ScrollToHash from "@/components/ScrollToHash";
import { Metadata } from "next";
import { Meta, Schema } from "@/once-ui/modules";

//generateStaticParams()에 getPosts의 슬러그 배열을 주고 스태틱 파라미터를 미리 생성
export async function generateStaticParams(): Promise<{ slug: string }[]> {
  //Promise<{ slug: string }[]> 타입 제네릭 타입 파라미터
  const posts = getPosts(["src", "app", "blog", "posts"]); //getPosts에서 받아온 객체에서 slug를 추출하여 posts 배열에 할당
  return posts.map((post) => ({
    //posts에서 받아온 객체에서 slug를 추출하여 post 배열에 할당
    slug: post.slug,
  }));
}
//사용자가 특정 포스트를 방문할 때 메타데이터를 생성 or export biled시에 메타데이터를 생성
export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string | string[] }>;
}): Promise<Metadata> {
  const routeParams = await params; // Next.js App Router에서 동적 경로(/blog/[slug])의 값(slug)을 params라는 객체로 제공하고,이 비동기 파라미터를 await로 풀어서 routeParams에 할당한다.
  const slugPath = Array.isArray(routeParams.slug) // 경로가 배열인지 확인하고 slugPath에 URL 경로를 할당
    ? routeParams.slug.join("/") // 배열이면 배열의 요소를 결합 routeParams.slug = ["foo", "bar"] => ["foo/bar"]
    : routeParams.slug || ""; // 배열이 아니면 경로를 반환 routeParams.slug = ["foo"] => ["foo"]

  const posts = getPosts(["src", "app", "blog", "posts"]);
  let post = posts.find((post) => post.slug === slugPath); // 슬러그 벨류가 slugPath와 일치하는 포스트 객체를 반환

  if (!post) return {};

  return Meta.generate({
    title: post.metadata.title, // 포스트 객체의 메타데이터에서 title을 가져옴
    description: post.metadata.summary, // 포스트 객체의 메타데이터에서 summary를 가져옴
    baseURL: baseURL, // 베이스 URL을 가져옴
    image: post.metadata.image // 포스트 객체의 메타데이터에서 image를 가져옴
      ? `${baseURL}${post.metadata.image}` // 이미지가 있으면 이미지 경로를 가져옴
      : `${baseURL}/og?title=${post.metadata.title}`, // 이미지가 없으면 타이틀을 가져오고 og로 이미지 생성
    path: `${blog.path}/${post.slug}`, // import한 blog의 객체(resources/index.ts<=content.js)의 path와 포스트 슬러그를 결합하여 포스트의 고유 경로를 생성
  });
}

export default async function Blog({ params }: { params: Promise<{ slug: string | string[] }> }) {
  const routeParams = await params;
  const slugPath = Array.isArray(routeParams.slug)
    ? routeParams.slug.join("/")
    : routeParams.slug || "";

  let post = getPosts(["src", "app", "blog", "posts"]).find((post) => post.slug === slugPath);

  if (!post) {
    notFound();
  }

  const avatars =
    post.metadata.team?.map((person) => ({
      src: person.avatar, // 포스트 객체의 메타데이터에서 team 배열의 각 객체에서 avatar(이미지경로)를 가져옴
    })) || [];

  return (
    <Row fillWidth>
      <Row maxWidth={12} hide="m" />
      <Row fillWidth horizontal="center">
        <Column as="section" maxWidth="xs" gap="l">
          {/* 블로그 포스트 스키마 SEO 정보 제공*/}
          <Schema
            as="blogPosting"
            baseURL={baseURL}
            path={`${blog.path}/${post.slug}`}
            title={post.metadata.title}
            description={post.metadata.summary}
            datePublished={post.metadata.publishedAt}
            dateModified={post.metadata.publishedAt}
            image={`${baseURL}/og?title=${encodeURIComponent(post.metadata.title)}`}
            author={{
              name: person.name,
              url: `${baseURL}${about.path}`,
              image: `${baseURL}${person.avatar}`,
            }}
          />
          {/* 블로그로 돌아가기 버튼 */}
          <Button
            data-border="rounded"
            href="/blog"
            weight="default"
            variant="tertiary"
            size="s"
            prefixIcon="chevronLeft"
          >
            Posts
          </Button>
          {/* 포스트 타이틀 색션 */}
          <Heading variant="display-strong-s">{post.metadata.title}</Heading>
          {/* 포스트 작성자 색션 */}
          <Row gap="12" vertical="center">
            {avatars.length > 0 && <AvatarGroup size="s" avatars={avatars} />}
            <Text variant="body-default-s" onBackground="neutral-weak">
              {post.metadata.publishedAt && formatDate(post.metadata.publishedAt)}{" "}
              {/* 포스트 작성일 */}
            </Text>
          </Row>
          {/* 포스트 컨텐츠 색션 */}
          <Column as="article" fillWidth>
            {/* 마크다운으로 작성된 파일을 읽어서 렌더링 */}
            <CustomMDX source={post.content} />
          </Column>
          <ScrollToHash />
        </Column>
      </Row>
      <Column maxWidth={12} paddingLeft="40" fitHeight position="sticky" top="80" gap="16" hide="m">
        <Row
          gap="12"
          paddingLeft="2"
          vertical="center"
          onBackground="neutral-medium"
          textVariant="label-default-s"
        >
          <Icon name="document" size="xs" />
          On this page
        </Row>
        <HeadingNav fitHeight />
      </Column>
    </Row>
  );
}
