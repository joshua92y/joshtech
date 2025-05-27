"use client";

import { useEffect, useState } from "react";
import { routes, protectedRoutes } from "@/app/resources";
import {
  Flex,
  Spinner,
  Button,
  Heading,
  Column,
  PasswordInput,
} from "@/once-ui/components";
import NotFound from "@/app/not-found";

interface RouteGuardProps {
  children: React.ReactNode;
}

const RouteGuard: React.FC<RouteGuardProps> = ({ children }) => {
  const [pathname, setPathname] = useState(""); // 현재 경로 저장용
  const [isRouteEnabled, setIsRouteEnabled] = useState(false); // 유효한 경로인지 여부
  const [isPasswordRequired, setIsPasswordRequired] = useState(false); // 비밀번호 보호 여부
  const [isAuthenticated, setIsAuthenticated] = useState(false); // 인증 상태
  const [password, setPassword] = useState(""); // 입력된 비밀번호
  const [error, setError] = useState<string | undefined>(undefined); // 에러 메시지
  const [loading, setLoading] = useState(true); // 전체 로딩 상태

  // ✅ 클라이언트에서 window 객체를 통해 현재 경로를 설정
  useEffect(() => {
    if (typeof window !== "undefined") {
      setPathname(window.location.pathname);
    }
  }, []);

  // ✅ 경로가 바뀔 때마다 라우팅/인증 상태 확인
  useEffect(() => {
    if (!pathname) return;

    const performChecks = async () => {
      setLoading(true);

      // ✅ 이전 상태 초기화 (다른 경로로 전환될 경우를 대비)
      setIsRouteEnabled(false);
      setIsPasswordRequired(false);
      setIsAuthenticated(false);
      setError(undefined);

      // ✅ 정적 routes 또는 dynamicRoutes에 포함되어 있는지 확인
      const checkRouteEnabled = (path: string): boolean => {
        if (path in routes) return routes[path as keyof typeof routes];

        const dynamicRoutes = ["/blog", "/work"] as const;
        return dynamicRoutes.some(
          (route) => path.startsWith(route) && routes[route]
        );
      };

      const routeEnabled = checkRouteEnabled(pathname);
      setIsRouteEnabled(routeEnabled);

      // ✅ 보호된 경로인 경우 인증 상태 확인 요청
      if (protectedRoutes[pathname as keyof typeof protectedRoutes]) {
        setIsPasswordRequired(true);

        try {
          const response = await fetch(
            "https://api.joshuatech.dev/security/check-auth",
            {
              method: "GET",
              credentials: "include", // ✅ 쿠키 포함 필수
            }
          );
          setIsAuthenticated(response.ok); // 200이면 인증됨
        } catch (err) {
          console.error("❌ 인증 확인 실패:", err);
        }
      }

      setLoading(false);
    };

    performChecks();
  }, [pathname]);

  // ✅ 비밀번호 제출 시 서버 인증 요청
  const handlePasswordSubmit = async () => {
    try {
      const response = await fetch(
        "https://api.joshuatech.dev/security/authenticate",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
          body: JSON.stringify({ password }),
        }
      );

      if (response.ok) {
        setIsAuthenticated(true);
        setError(undefined);
      } else {
        setError("Incorrect password");
      }
    } catch (err) {
      setError("Network error");
    }
  };

  // ✅ 로딩 중일 때 스피너 표시
  if (loading) {
    return (
      <Flex fillWidth paddingY="128" horizontal="center">
        <Spinner />
      </Flex>
    );
  }

  // ✅ 허용되지 않은 경로일 경우 NotFound 컴포넌트 표시
  if (!isRouteEnabled) {
    return <NotFound />;
  }

  // ✅ 인증이 필요한 경로지만 인증되지 않은 경우 비밀번호 폼 표시
  if (isPasswordRequired && !isAuthenticated) {
    return (
      <Column paddingY="128" maxWidth={24} gap="24" center>
        <Heading align="center" wrap="balance">
          This page is password protected
        </Heading>
        <Column fillWidth gap="8" horizontal="center">
          <PasswordInput
            id="password"
            label="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            errorMessage={error}
          />
          <Button onClick={handlePasswordSubmit}>Submit</Button>
        </Column>
      </Column>
    );
  }

  // ✅ 인증 통과 및 경로 유효 → 원래 콘텐츠 렌더링
  return <>{children}</>;
};

export { RouteGuard };
