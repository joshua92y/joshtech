//src/components/ScrollToHash.tsx
"use client"; // 클라이언트 컴포넌트로 선언

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function ScrollToHash() { //클라이언트에서 ScrollToHash 호출시 작동
  const router = useRouter(); //useRouter 훅 사용

  useEffect(() => {
    // URL에서 해시 가져오기
    const hash = window.location.hash;
    if (hash) {
      // '#' 기호 제거
      const id = hash.replace("#", "");
      const element = document.getElementById(id); //id 태그 요소 가져오기
      if (element) { //해시를 제거한 url에 해당하는 id 태그 요소가 있으면
        element.scrollIntoView({ behavior: "smooth" }); // 해당 태그 요소가 보이도록 부드럽게 스크롤 이동
      }
    }
  }, [router]); //router(URL)가 변경될 때마다 실행

  return null;
}
