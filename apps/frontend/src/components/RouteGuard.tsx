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
  const [pathname, setPathname] = useState(""); // 현재 경로
  const [isRouteEnabled, setIsRouteEnabled] = useState(false); // 라우팅 허용 여부
  const [isPasswordRequired, setIsPasswordRequired] = useState(false); // 보호 여부
  const [isAuthenticated, setIsAuthenticated] = useState(false); // 인증 상태
  const [password, setPassword] = useState(""); // 입력된 비밀번호
  const [error, setError] = useState<string | undefined>(undefined); // 에러 메시지
  const [loading, setLoading] = useState(true); // 로딩 상태

  // ✅ 경로 초기 추출 (CSR only)
  useEffect(() => {
    if (typeof window !== "undefined") {
      setPathname(window.location.pathname);
    }
  }, []);

  // ✅ 경로 변경 감지 → 보호 여부 및 인증 확인
  useEffect(() => {
    if (!pathname) return;

    const performChecks = async () => {
      setLoading(true);

      // 상태 초기화
      setIsRouteEnabled(false);
      setIsPasswordRequired(false);
      setIsAuthenticated(false);
      setError(undefined);

      // 정적 또는 동적 라우트 여부 확인
      const checkRouteEnabled = (path: string): boolean => {
        if (path in routes) return routes[path as keyof typeof routes];

        const dynamicRoutes = ["/blog", "/work"] as const;
        return dynamicRoutes.some(
          (route) => path.startsWith(route) && Boolean(routes[route])
        );
      };

      const routeEnabled = checkRouteEnabled(pathname);
      setIsRouteEnabled(routeEnabled);

      // ✅ 보호된 경로일 경우만 인증 확인
      if (protectedRoutes[pathname as keyof typeof protectedRoutes]) {
        setIsPasswordRequired(true);

        try {
          const response = await fetch("https://api.joshuatech.dev/security/check-auth", {
            method: "GET",
            credentials: "include",
          });

          setIsAuthenticated(response.ok); // 200이면 인증 완료
        } catch (err) {
          console.error("❌ 인증 확인 실패:", err);
        }
      }

      setLoading(false);
    };

    performChecks();
  }, [pathname]);

  // ✅ 비밀번호 제출 → 인증 API 호출
  const handlePasswordSubmit = async () => {
    try {
      const response = await fetch("https://api.joshuatech.dev/security/authenticate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ password }),
      });

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

  // ✅ 로딩 중
  if (loading) {
    return (
      <Flex fillWidth paddingY="128" horizontal="center">
        <Spinner />
      </Flex>
    );
  }

  // ✅ 비허용 경로
  if (!isRouteEnabled) {
    return <NotFound />;
  }

  // ✅ 보호된 경로지만 인증되지 않음 → 비밀번호 폼
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

  // ✅ 통과 시 children 렌더링
  return <>{children}</>;
};

export { RouteGuard };
