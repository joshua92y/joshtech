//src/app/utils/utils.ts
import fs from "fs";
import path from "path";
import matter from "gray-matter"; //gray-matter는 마크다운 파일에서 --- 구분자로 시작하는 YAML 블록을 파싱

// 팀 타입 정의
type Team = {
  name: string;
  role: string;
  avatar: string;
  linkedIn: string;
};

// 메타데이터는 포스트의 정보를 담고 있는 객체 타입 정의
type Metadata = { 
  title: string;
  publishedAt: string;
  summary: string;
  image?: string;
  images: string[];
  tag?: string;
  team: Team[];
  link?: string;
};

import { notFound } from "next/navigation";

//getMDXData에서 호출되고 postsdir경로(/project-root/src/app/blog/posts)를 받아와서 디렉토리의 모든 파일을 읽고 .mdx로 끝나는 파일명을 반환
function getMDXFiles(dir: string) {
  if (!fs.existsSync(dir)) { //fs.existsSync(dir) 디렉토리가 존재하는지 확인_boolean_node.js함수
    notFound(); // 디렉토리가 없으면 404 페이지로 리다이렉트
  }
  
  return fs.readdirSync(dir).filter((file) => path.extname(file) === ".mdx"); // 예시 결과: ["seo.mdx", "work.mdx", "blog.mdx".....]
}
//getMDXFiles에서 호출되고 postsdir경로와 파일명을 받아와서 파일을 읽고 메타데이터와 콘텐츠를 반환
function readMDXFile(filePath: string) {
  if (!fs.existsSync(filePath)) { //fs.existsSync(filePath) 파일이 존재하는지 확인_boolean_node.js함수
    notFound(); // 파일이 없으면 404 페이지로 리다이렉트
  }

  const rawContent = fs.readFileSync(filePath, "utf-8"); //fs.readFileSync(filePath, "utf-8") 파일을 읽고 문자열로 반환
  const { data, content } = matter(rawContent); // --- 구분자로 데이터와 콘텐츠를 분리

  const metadata: Metadata = {
    title: data.title || "", // 데이터에서 타이틀을 가져오고 없으면 빈 문자열로 초기화
    publishedAt: data.publishedAt, // 데이터에서 게시일을 가져오고 없으면 빈 문자열로 초기화
    summary: data.summary || "", // 데이터에서 요약을 가져오고 없으면 빈 문자열로 초기화
    image: data.image || "", // 데이터에서 이미지를 가져오고 없으면 빈 문자열로 초기화
    images: data.images || [], // 데이터에서 이미지 배열을 가져오고 없으면 빈 배열로 초기화
    tag: data.tag || [], // 데이터에서 태그를 가져오고 없으면 빈 배열로 초기화
    team: data.team || [], // 데이터에서 팀을 가져오고 없으면 빈 배열로 초기화
    link: data.link || "", // 데이터에서 링크를 가져오고 없으면 빈 문자열로 초기화
  };

  return { metadata, content }; // 메타데이터와 콘텐츠를 반환
}
//getPosts에서 호출되고 postsdir경로를 받아와서 getMDXFiles로 전달 후 변환된 배열을 맵핑(메타데이터, 콘텐츠)=>readMDXFile 슬러그=> 파일명
function getMDXData(dir: string) {
  const mdxFiles = getMDXFiles(dir); // 예시 결과: ["seo.mdx", "work.mdx", "blog.mdx".....]
  return mdxFiles.map((file) => { // 예시 결과: [{metadata, slug, content}, {metadata, slug, content}, {metadata, slug, content}.....]
    const { metadata, content } = readMDXFile(path.join(dir, file)); // 파일 경로를 만들고 readMDXFile로 전달 후 메타데이터와 콘텐츠를 반환
    const slug = path.basename(file, path.extname(file)); // basename로 전체 파일 이름과 path.extname(file)로 파일 확장자를 넣어서 제거한 파일이름을 슬러그로 변환

    return {
      metadata,
      slug,
      content,
    };
  });
}

//페이지에서 getPosts호출 postsdir경로 배열을 받아와서 디렉토리 경로를 만들고 getMDXData로 전달
export function getPosts(customPath = ["", "", "", ""]) {
  const postsDir = path.join(process.cwd(), ...customPath);
  // 예시 결과: /project-root/src/app/blog/posts
  return getMDXData(postsDir); // 예시 결과: 맵핑된 배열  [{metadata: { title: "SEO 글", ... },, slug: "seo",content: "# SEO 글 내용"}, {metadata, slug, content}, {metadata, slug, content}.....]
}
