// src/hooks/useClientPathTracker.ts
"use client";

import { useEffect, useState } from "react";

/**
 * 클라이언트에서 현재 경로(window.location.pathname)를 상태로 추적
 * CSR 환경에서 pushState/replaceState/popstate 이벤트를 감지함
 */
export function useClientPathTracker(): string {
  const [pathname, setPathname] = useState("");

  useEffect(() => {
    const updatePathname = () => {
      setPathname(window.location.pathname);
    };

    updatePathname(); // 초기 경로 설정

    // pushState, replaceState 패치하여 커스텀 이벤트 발생
    const patchHistoryMethod = (method: "pushState" | "replaceState") => {
      const original = history[method];
      history[method] = function (...args) {
        const result = original.apply(this, args);
        window.dispatchEvent(new Event("locationchange"));
        return result;
      };
    };

    patchHistoryMethod("pushState");
    patchHistoryMethod("replaceState");

    window.addEventListener("popstate", updatePathname);
    window.addEventListener("locationchange", updatePathname);

    return () => {
      window.removeEventListener("popstate", updatePathname);
      window.removeEventListener("locationchange", updatePathname);
    };
  }, []);

  return pathname;
}
